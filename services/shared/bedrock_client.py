import boto3, os, json

# Create the client in your Bedrock region (you've been using us-east-2)
bedrock = boto3.client("bedrock-runtime", region_name=os.getenv("BEDROCK_REGION","us-east-2"))

def call_bedrock_claude(prompt,
                        inference_profile_id=None,
                        model_id=None,
                        max_tokens=800):
    """
    Prefer inference_profile_id (Bedrock routing). Fallback to model_id only if needed.
    You can set BEDROCK_INFERENCE_PROFILE or BEDROCK_MODEL_ID in Lambda env.
    """
    inference_profile_id = inference_profile_id or os.getenv("BEDROCK_INFERENCE_PROFILE")
    model_id = model_id or os.getenv("BEDROCK_MODEL_ID")  # only used if profile not provided

    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": max_tokens,
        "messages": [{"role": "user", "content": prompt}],
    }

    if inference_profile_id:
        resp = bedrock.invoke_model(inferenceProfileId=inference_profile_id,
                                    body=json.dumps(body))
    else:
        # Legacy path (only works if that model supports on-demand in your account)
        resp = bedrock.invoke_model(modelId=model_id, body=json.dumps(body))

    out = json.loads(resp["body"].read())
    # Return text from the first content block
    return out["content"][0]["text"]

