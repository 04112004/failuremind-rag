import json
try:
    from langchain_groq import ChatGroq  # type: ignore
except Exception as e:
    raise ImportError(
        "Missing dependency: install with `pip install langchain-groq`"
    ) from e
from app.retrievers import load_retrievers
from app.prompts import RISK_PROMPT
from app.risk import compute_risk_score

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0
)


def run_rag(question: str):
    retrievers = load_retrievers()   # ✅ load at runtime, not import time
    contexts = []

    for name, r in retrievers.items():
        if r is None:
            continue
        docs = r.invoke(question)
        contexts.extend([d.page_content for d in docs])

    # ✅ HARD SAFETY CHECK
    if not contexts:
        return {
            "risk_level": "UNKNOWN",
            "risk_score": 0,
            "likely_failure": "Knowledge base not initialized",
            "evidence": [],
            "recommended_actions": [
                "Upload data",
                "Run ingestion pipeline",
                "Rebuild vector store"
            ]
        }

    prompt = RISK_PROMPT.format(
        context="\n".join(contexts[:6]),  # limit context
        question=question
    )

    response = llm.invoke(prompt)
    raw = response.content.strip()

    try:
        parsed = json.loads(raw)
    except Exception:
        parsed = {
            "likely_failure": "Uncertain system behavior",
            "evidence": contexts[:3],
            "recommended_actions": [
                "Add monitoring",
                "Improve maintenance schedule"
            ]
        }

    risk_score = compute_risk_score(contexts, parsed)

    parsed["risk_level"] = (
        "HIGH" if risk_score >= 0.7
        else "MEDIUM" if risk_score >= 0.4
        else "LOW"
    )
    parsed["risk_score"] = risk_score

    return parsed
