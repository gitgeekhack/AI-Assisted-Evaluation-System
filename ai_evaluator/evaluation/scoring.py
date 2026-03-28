# evaluation/scoring.py

from langchain_community.llms import Ollama
from utils.json_parser import safe_parse

llm = Ollama(model="llama3")

RUBRIC = [
    "Problem Understanding",
    "Technical Approach",
    "Implementation Quality",
    "Innovation / Originality",
    "Communication & Demo Clarity"
]


def format_evidence(evidence_chunks):
    """
    Convert retrieved evidence into structured text with citations
    """
    formatted = []

    for e in evidence_chunks:
        source = e.get("source", "unknown")
        content = e.get("content", "")

        formatted.append(f"[{source}] {content}")

    return "\n\n".join(formatted)


def build_prompt(evidence_text, prototype_data=None, claim_validation=None):
    """
    Build scoring prompt with strict grounding
    """

    prototype_section = ""
    if prototype_data:
        prototype_section = f"""
PROTOTYPE VALIDATION:
- Accessible: {prototype_data.get("accessible")}
- Loads: {prototype_data.get("loads")}
- Navigation: {prototype_data.get("flows", {}).get("navigation_working")}
- Core Actions: {prototype_data.get("flows", {}).get("core_actions_detected")}
- Data Processing: {prototype_data.get("data_processing_signals")}
"""

    claim_section = ""
    if claim_validation:
        claim_section = f"""
CLAIM VALIDATION SUMMARY:
{claim_validation}
"""

    return f"""
You are an expert AI evaluator.

You MUST evaluate STRICTLY based on evidence.

DO NOT:
- hallucinate
- assume missing information
- give generic reasoning

EVIDENCE:
{evidence_text}

{prototype_section}

{claim_section}

RUBRIC:
1. Problem Understanding
2. Technical Approach
3. Implementation Quality
4. Innovation / Originality
5. Communication & Demo Clarity

TASK:
- Score EACH criterion from 1 to 5
- Justify using ONLY evidence
- Add citations (source IDs like slide_3, video_00:02:10, file.py:chunk_1)

CONFIDENCE RULE:
- 0.8–1.0 → strong multi-source evidence
- 0.5–0.8 → partial evidence
- <0.5 → weak evidence

OUTPUT RULES (VERY IMPORTANT):
- Return ONLY valid JSON
- No explanation outside JSON
- Follow structure EXACTLY

OUTPUT FORMAT (STRICT JSON):
{{
  "scores": [
    {{
      "criterion": "Problem Understanding",
      "score": 1,
      "reasoning": "...",
      "citations": ["..."],
      "confidence": 0.0
    }}
  ]
}}
"""


def score_submission(evidence_chunks, prototype_data=None, claim_validation=None):
    """
    Main scoring function

    Inputs:
    - evidence_chunks (retrieved from vector DB)
    - prototype_data (URL validation output)
    - claim_validation (Step 5 output)

    Output:
    - structured scoring JSON
    """

    evidence_text = format_evidence(evidence_chunks)

    prompt = build_prompt(
        evidence_text,
        prototype_data=prototype_data,
        claim_validation=claim_validation
    )

    response = llm.invoke(prompt)

    return safe_parse(response)