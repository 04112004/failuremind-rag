import json
from langchain_groq import ChatGroq
from app.retrievers import load_retrievers
from app.prompts import RISK_PROMPT
from app.risk import compute_risk_score

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0
)

def run_rag(question: str):
    retrievers = load_retrievers()

    contexts = []

    for name, r in retrievers.items():
        if r is None:
            continue   # ✅ CRITICAL FIX
        docs = r.invoke(question)
        contexts.extend([d.page_content for d in docs])

    # If no context at all → graceful fallback
    if not contexts:
        return {
            "risk_level": "UNKNOWN",
            "risk_score": 0.0,
            "likely_failure": "Knowledge base not initialized",
            "evidence": [],
            "recommended_actions": ["Upload data and rebuild vector store"]
        }

    prompt = RISK_PROMPT.format(
        context="\n".join(contexts),
        question=question
    )

    response = llm.invoke(prompt)
    raw = response.content.strip()

    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        parsed = {
            "risk_level": "MEDIUM",
            "likely_failure": "Uncertain system behavior",
            "evidence": contexts[:3],
            "recommended_actions": ["Add monitoring", "Improve validation"]
        }

    risk_score = compute_risk_score(contexts, parsed)

    if risk_score >= 0.7:
        level = "HIGH"
    elif risk_score >= 0.4:
        level = "MEDIUM"
    else:
        level = "LOW"

    parsed["risk_level"] = level
    parsed["risk_score"] = risk_score

    return parsed



