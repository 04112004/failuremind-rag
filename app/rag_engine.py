import json
from langchain_groq import ChatGroq
from app.retrievers import load_retrievers
from app.prompts import RISK_PROMPT
from app.risk import compute_risk_score

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0
)

retrievers = load_retrievers()

def is_safe_question(question: str) -> bool:
    q = question.lower()

    safe_phrases = [
        "working as expected",
        "no issues",
        "stable",
        "normal operation",
        "operating normally",
        "healthy",
        "all good",
        "running fine"
    ]

    return any(p in q for p in safe_phrases)


def run_rag(question: str):
    # ---------- HARD LOW GATE ----------
    if is_safe_question(question):
        return {
            "risk_level": "LOW",
            "risk_score": 0.0,
            "likely_failure": "No failure detected",
            "evidence": [],
            "recommended_actions": ["Continue monitoring"]
        }

    # ---------- RAG ----------
    contexts = []
    for r in retrievers.values():
        docs = r.invoke(question)
        contexts.extend([d.page_content for d in docs])

    prompt = RISK_PROMPT.format(
        context="\n".join(contexts),
        question=question
    )

    response = llm.invoke(prompt)
    raw = response.content.strip()

    try:
        parsed = json.loads(raw)
    except Exception:
        parsed = {
            "likely_failure": "Uncertain behavior",
            "evidence": contexts[:2],
            "recommended_actions": ["Add monitoring"]
        }

    # ---------- SCORE ----------
    risk_score = compute_risk_score(contexts, parsed)

    # ---------- SEVERITY (USER + LLM ONLY) ----------
    severity_text = (
        question + " " +
        parsed.get("likely_failure", "")
    ).lower()

    severe_keywords = [
        "failure", "failed", "silent", "corrupted",
        "crash", "shutdown", "timeout", "drift", "misalignment"
    ]

    has_severe_signal = any(k in severity_text for k in severe_keywords)

    # ---------- FINAL LEVEL ----------
    if has_severe_signal and risk_score >= 0.6:
        risk_level = "HIGH"
    elif risk_score >= 0.3:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    parsed["risk_level"] = risk_level
    parsed["risk_score"] = round(risk_score, 2)

    return parsed
