# evaluation/claim_validation.py

from langchain_community.llms import Ollama
from utils.json_parser import safe_parse

llm = Ollama(model="llama3")

def format_evidence_by_source(evidence_chunks):
    """
    Groups evidence by source type (deck, video, code)
    """
    grouped = {
        "deck": [],
        "video": [],
        "code": []
    }

    for e in evidence_chunks:
        source = e.get("source", "")
        content = e.get("content", "")

        if "slide" in source:
            grouped["deck"].append(f"[{source}] {content}")
        elif "video" in source:
            grouped["video"].append(f"[{source}] {content}")
        else:
            grouped["code"].append(f"[{source}] {content}")

    return grouped


def validate_claims(evidence_chunks, prototype_data=None):
    """
    Cross-reference claims across:
    - deck
    - video
    - code
    - prototype

    Returns:
    - claim validation report
    - missing / weak evidence flags
    """

    grouped = format_evidence_by_source(evidence_chunks)

    deck_text = "\n\n".join(grouped["deck"])
    video_text = "\n\n".join(grouped["video"])
    code_text = "\n\n".join(grouped["code"])

    prototype_section = ""
    if prototype_data:
        prototype_section = f"""
PROTOTYPE SIGNALS:
- Accessible: {prototype_data.get("accessible")}
- Loads: {prototype_data.get("loads")}
- Buttons: {prototype_data.get("ui_elements", {}).get("buttons", [])}
- Inputs: {prototype_data.get("ui_elements", {}).get("inputs", [])}
- Core Actions: {prototype_data.get("flows", {}).get("core_actions_detected")}
- Data Signals: {prototype_data.get("data_processing_signals", [])}
"""

    prompt = f"""
You are an expert AI evaluator.

Your task is to STRICTLY validate claims using evidence.

DATA SOURCES:

DECK (claims):
{deck_text}

VIDEO (demonstration evidence):
{video_text}

CODE (implementation evidence):
{code_text}

{prototype_section}

TASK:

1. Extract ALL claims/features from DECK.
2. For EACH claim:
   - Check if implemented in CODE
   - Check if shown in VIDEO
   - Check if working in PROTOTYPE

3. Assign status:
   - verified
   - partially_verified
   - not_verified

4. Identify issues:
   - Missing implementation (claimed but not in code)
   - Not demonstrated (in code but not shown in video)
   - Broken/weak functionality (not working in prototype)
   - Weak evidence (unclear or partial support)

OUTPUT RULES (VERY IMPORTANT):
- Return ONLY valid JSON
- No explanations outside JSON
- Follow structure EXACTLY

OUTPUT FORMAT (STRICT JSON):
{{
  "claims_analysis": [
    {{
      "claim": "...",
      "status": "verified | partially_verified | not_verified",
      "evidence": {{
        "deck": ["slide_x"],
        "video": ["video_00:01:10"],
        "code": ["file.py:chunk_1"],
        "prototype": ["button_detected"]
      }},
      "issues": ["missing_in_code", "not_in_video", "not_working_in_app"]
    }}
  ],
  "summary": {{
    "total_claims": 0,
    "verified": 0,
    "partial": 0,
    "not_verified": 0
  }},
  "missing_features": ["..."],
  "weak_evidence_flags": ["..."]
}}

IMPORTANT:
- Use ONLY given evidence
- Do NOT hallucinate
- Be strict in validation
"""

    response = llm.invoke(prompt)

    return safe_parse(response)