# evaluation/summary.py

from langchain_community.llms import Ollama
from utils.json_parser import safe_parse

llm = Ollama(model="llama3")

def format_evidence(evidence_chunks):
    """
    Convert retrieved evidence into structured text for LLM
    """
    formatted = []

    for e in evidence_chunks:
        source = e.get("source", "unknown")
        content = e.get("content", "")

        formatted.append(f"[{source}]\n{content}")

    return "\n\n".join(formatted)


def generate_unified_summary(evidence_chunks, prototype_data=None):
    """
    Builds unified understanding of submission

    Inputs:
    - evidence_chunks (from retrieval)
    - prototype_data (URL validation output)

    Output:
    - structured summary:
        - problem
        - solution
        - features
        - implementation depth
    """

    formatted_evidence = format_evidence(evidence_chunks)

    prototype_section = ""
    if prototype_data:
        prototype_section = f"""
        Prototype Validation Signals:
        - Accessible: {prototype_data.get("accessible")}
        - Loads: {prototype_data.get("loads")}
        - Buttons: {prototype_data.get("ui_elements", {}).get("buttons", [])}
        - Inputs: {prototype_data.get("ui_elements", {}).get("inputs", [])}
        - Core Actions Detected: {prototype_data.get("flows", {}).get("core_actions_detected")}
        - Data Processing Signals: {prototype_data.get("data_processing_signals", [])}
        """

    prompt = f"""
You are an expert AI evaluator.

Your task is to build a UNIFIED understanding from multiple sources.

SOURCES:
- Deck
- Video
- Code
- Prototype signals

IMPORTANT RULES:
- Use ONLY the provided evidence
- Do NOT hallucinate
- Merge signals across sources
- Be precise and structured

EVIDENCE:
{formatted_evidence}

{prototype_section}

TASK:

1. Identify the PROBLEM being solved
2. Identify the SOLUTION approach
3. Extract ALL FEATURES (deduplicated)
4. Evaluate IMPLEMENTATION DEPTH:
   - low → minimal / incomplete code
   - medium → working core logic
   - high → full system with multiple components

OUTPUT RULES (VERY IMPORTANT):
- Return ONLY valid JSON
- No explanation outside JSON
- Be precise and grounded in evidence

OUTPUT FORMAT (STRICT JSON):
{{
  "problem": "...",
  "solution": "...",
  "features": ["...", "..."],
  "implementation_depth": {{
      "level": "low | medium | high",
      "justification": "..."
  }}
}}
"""

    response = llm.invoke(prompt)

    return safe_parse(response)