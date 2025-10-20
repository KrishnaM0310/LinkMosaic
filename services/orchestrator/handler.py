import sys, os
sys.path.append("/var/task/package")

import json
import boto3
from io import BytesIO
from urllib.parse import unquote_plus
from PyPDF2 import PdfReader

# Initialize clients
lambda_client = boto3.client("lambda")
s3 = boto3.client("s3")

def call_lambda(function_name, payload):
    """Invoke another Lambda synchronously and return parsed response."""
    response = lambda_client.invoke(
        FunctionName=function_name,
        InvocationType="RequestResponse",
        Payload=json.dumps(payload)
    )
    return json.loads(response["Payload"].read())

def get_text_from_s3(event):
    """Extract text from PDF or TXT file uploaded to S3."""
    record = event["Records"][0]
    bucket = record["s3"]["bucket"]["name"]
    key = unquote_plus(record["s3"]["object"]["key"])
    obj = s3.get_object(Bucket=bucket, Key=key)
    body = obj["Body"].read()

    if key.lower().endswith(".pdf"):
        reader = PdfReader(BytesIO(body))
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
        return text
    elif key.lower().endswith(".txt"):
        return body.decode("utf-8")
    else:
        return ""

def handler(event, _):
    """Main orchestrator entrypoint for S3, CLI, or Bedrock events."""
    # 🔹 Normalize all possible event shapes
    if "Records" in event:  # S3 trigger
        text_input = get_text_from_s3(event)
    elif "bucket" in event and "key" in event:  # direct CLI invoke
        bucket = event["bucket"]
        key = event["key"]
        obj = s3.get_object(Bucket=bucket, Key=key)
        body = obj["Body"].read()
        if key.lower().endswith(".pdf"):
            reader = PdfReader(BytesIO(body))
            text_input = "\n".join(page.extract_text() or "" for page in reader.pages)
        else:
            text_input = body.decode("utf-8")
    elif "inputs" in event and "text" in event["inputs"]:  # Bedrock-style event
        text_input = event["inputs"]["text"]
    else:
        raise ValueError(f"Unsupported event shape: {event}")

    # 1️⃣ Summarize
    summaries_resp = call_lambda("LinkMosaic_SummaryExtractor", {"inputs": {"text": text_input}})
    summaries = summaries_resp.get("summary", "")
    print("Summaries:", summaries)

    # 2️⃣ Get embeddings
    emb_resp = call_lambda("LinkMosaic_EmbeddingTool", {"inputs": {"texts": [summaries]}})
    embeddings = emb_resp.get("embeddings", [])
    print("Embeddings:", embeddings)

    # 3️⃣ Cluster
    cluster_resp = call_lambda("LinkMosaic_ClusterTool", {"inputs": {"embeddings": embeddings}})
    clusters = cluster_resp.get("clusters", [])
    print("Clusters:", clusters)

    # 4️⃣ Infer relationships
    rel_resp = call_lambda("LinkMosaic_RelationshipInfer", {"inputs": {"summaries": [summaries]}})
    edges = rel_resp.get("edges", [])
    print("Edges:", edges)

    # 5️⃣ Build map
    map_resp = call_lambda("LinkMosaic_MapBuilder", {
        "inputs": {
            "summaries": [summaries],
            "clusters": clusters,
            "edges": edges
        }
    })
    print("🗺️ Map Response:", map_resp)

    # 6️⃣ Return orchestrator output
    return {
        "status": "ok",
        "map_output": map_resp
    }

