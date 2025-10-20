import boto3, json, os
rt = boto3.client("sagemaker-runtime", region_name=os.getenv("AWS_REGION", "us-east-2"))

def handler(event, _):
    texts = event["inputs"]["texts"]
    payload = {"inputs": texts}
    resp = rt.invoke_endpoint(
        EndpointName=os.getenv("SM_ENDPOINT", "linkmosaic-embeddings"),
        ContentType="application/json",
        Body=json.dumps(payload)
    )
    arr = json.loads(resp["Body"].read())
    vectors = [x[0] if isinstance(x[0], list) else x for x in arr]
    return {"embeddings": vectors}

