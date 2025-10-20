import json
from services.shared.bedrock_client import call_bedrock_claude

PROMPT = """Summarize the following text in 3–5 concise bullets capturing the core ideas.
Return only bullets prefixed with '- '.
TEXT:
"""

def handler(event, _):
    text = event["inputs"]["text"][:50000]  # cap for safety
    summary = call_bedrock_claude(PROMPT + text)
    return {"summary": summary}

