def compute_risk_score(contexts: list[str], llm_output: dict) -> float:
    score = 0.0

    # 1️⃣ Retrieval signal
    if len(contexts) >= 5:
        score += 0.3
    elif len(contexts) >= 3:
        score += 0.2
    else:
        score += 0.1

    # 2️⃣ Keyword severity
    severe_keywords = [
        "silent", "degraded", "corrupted", "hallucinated",
        "timeout", "drift", "failure", "misalignment"
    ]

    text_blob = " ".join(contexts).lower()
    if any(k in text_blob for k in severe_keywords):
        score += 0.3

    # 3️⃣ Time-based risk (heuristic from text)
    if "days" in text_blob or "gradually" in text_blob:
        score += 0.2

    # 4️⃣ Missing controls (from LLM output)
    actions = " ".join(llm_output.get("recommended_actions", [])).lower()
    if "monitor" in actions or "alert" in actions:
        score += 0.2

    # Clamp score
    return round(min(score, 1.0), 2)
