import json, os, uuid, boto3, time

s3 = boto3.client("s3", region_name=os.getenv("AWS_REGION", "us-east-2"))
MAP_BUCKET = os.getenv("MAP_BUCKET")

def handler(event, _):
    summaries = event["inputs"]["summaries"]
    clusters  = event["inputs"]["clusters"]
    edges     = event["inputs"]["edges"]

    nodes = []
    for i, (s, c) in enumerate(zip(summaries, clusters)):
        nodes.append({
            "id": str(i),
            "label": s.split("\n")[0][:120],
            "group": int(c)
        })

    links = []
    for e in edges:
        if "source" in e and "target" in e:
            links.append({
                "source": str(e["source"]),
                "target": str(e["target"]),
                "type": e.get("type", "similar"),
                "weight": float(e.get("weight", 0.5))
            })

    data = {"nodes": nodes, "links": links}
    key = f"maps/{int(time.time())}.json"
    s3.put_object(Bucket=MAP_BUCKET, Key=key, Body=json.dumps(data).encode("utf-8"),
                  ContentType="application/json")
    s3.put_object(Bucket=MAP_BUCKET, Key="latest_map.json",
                  Body=json.dumps(data).encode("utf-8"),
                  ContentType="application/json")
    return {"status": "ok", "map_key": key}

