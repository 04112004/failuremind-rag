from pydantic import BaseModel
from typing import List, Optional


# -------- INPUT --------
class RiskQuery(BaseModel):
    question: str


# -------- OUTPUT --------
class RiskAnalysis(BaseModel):
    risk_level: str
    risk_score: float
    likely_failure: str
    evidence: List[str]
    recommended_actions: List[str]


# -------- INTERNAL (Optional, but clean) --------
class FailureEvent(BaseModel):
    failure_id: str
    system_type: str
    stage: str
    description: str
    impact: str
    environment: List[str]
    time_to_failure_days: Optional[int]


class RootCause(BaseModel):
    cause_id: str
    failure_id: str
    root_cause: str
    why: str
    signals: List[str]


class FixAction(BaseModel):
    fix_id: str
    cause_id: str
    solution: str
    tools: List[str]
    preventive_actions: List[str]
    effectiveness: str
