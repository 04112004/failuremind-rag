def compute_risk_score(contexts: list[str], llm_output: dict) -> float:
    score = 0.0
    text = (
        " ".join(contexts) + " " +
        llm_output.get("likely_failure", "")
    ).lower()

    if any(k in text for k in [
        "failure", "failed", "silent",
        "corrupted", "crash", "shutdown", "timeout"
    ]):
        score += 0.5

    if any(k in text for k in [
        "overheating", "latency", "slow",
        "reduced performance", "intermittent"
    ]):
        score += 0.25

    if any(t in text for t in ["days", "weeks", "gradually", "over time"]):
        score += 0.15

    return round(min(score, 1.0), 2)


