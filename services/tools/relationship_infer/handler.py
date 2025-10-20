import json
from services.shared.bedrock_client import call_bedrock_claude

PROMPT = """You are building a knowledge graph. Given N short node summaries, infer conceptual links.
Types: "similar", "supports", "contradicts", "causes".
Return pure JSON array of edges: [{"source": i, "target": j, "type": "similar", "weight": 0.7}].
Use 0-based indices. Be selective; 1–3 edges per node is enough.

SUMMARIES:
"""

def handler(event, _):
    summaries = event["inputs"]["summaries"]
    joined = "\n".join([f"[{i}] {s}" for i, s in enumerate(summaries)])
    raw = call_bedrock_claude(PROMPT + joined)
    try:
        edges = json.loads(raw)
    except Exception:
        edges = []  # fallback if model output isn’t JSON
    return {"edges": edges}

