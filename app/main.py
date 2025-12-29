from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from app.schemas import RiskQuery, RiskAnalysis
from app.rag_engine import run_rag

app = FastAPI(title="FailureMind")

@app.post("/analyze", response_model=RiskAnalysis)
def analyze(query: RiskQuery):
    return run_rag(query.question)

