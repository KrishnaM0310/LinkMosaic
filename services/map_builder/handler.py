import json, boto3, os

s3 = boto3.client("s3")
MAP_BUCKET = os.environ.get("MAP_BUCKET", "linkmosaic-maps-krishnamehta")

def handler(event, _context):
    inputs = event.get("inputs", {})
    summaries = inputs.get("summaries", [""])
    clusters = inputs.get("clusters", [])
    edges = inputs.get("edges", [])

    # Create a simple map JSON object
    map_data = {
        "nodes": [{"id": i, "label": f"Cluster {i}", "summary": s}
                  for i, s in enumerate(summaries)],
        "edges": edges or [],
        "clusters": clusters or []
    }

    # Upload to S3 for easy viewing
    map_key = "maps/latest_map.json"
    s3.put_object(
        Bucket=MAP_BUCKET,
        Key=map_key,
        Body=json.dumps(map_data, indent=2),
        ContentType="application/json"
    )

    print(f"✅ Map uploaded to s3://{MAP_BUCKET}/{map_key}")
    return {
        "status": "ok",
        "map_s3_uri": f"s3://{MAP_BUCKET}/{map_key}",
        "map_data": map_data
    }

