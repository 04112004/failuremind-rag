RISK_PROMPT = """
You are an industrial reliability expert.

Use ONLY the context below.
If information is missing, infer conservatively.

Context:
{context}

User Question:
{question}

Respond ONLY in valid JSON:

{{
  "likely_failure": "string",
  "evidence": ["string"],
  "recommended_actions": ["string"]
}}
"""
