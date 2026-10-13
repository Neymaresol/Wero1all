from fastapi import FastAPI
from pydantic import BaseModel, Field
from datetime import datetime, timezone
from typing import List
from wero1divulgacao.planner import Offer, plan
from wero1divulgacao.intent import rank_offers
from wero1divulgacao.happy_path import simulate_happy_path

app = FastAPI(title="Wero1Divulgacao", version="0.4.0-dev")

class OfferInput(BaseModel):
    id: int
    title: str
    approved: bool = False
    active: bool = False
    affiliate_authorized: bool = False

class PlanRequest(BaseModel):
    campaign: str
    offers: List[OfferInput] = Field(default_factory=list, max_length=1000)
    limit: int = Field(default=10, ge=1, le=1000)

class IntentRequest(BaseModel):
    offers: List[OfferInput] = Field(default_factory=list, max_length=1000)
    public_queries: List[str] = Field(default_factory=list, max_length=100)
    trending_topics: List[str] = Field(default_factory=list, max_length=100)
    limit: int = Field(default=10, ge=1, le=1000)

@app.get("/health")
def health():
    return {"status":"ok","service":"wero1divulgacao","version":"0.4.0-dev",
            "mode":"staging","time":datetime.now(timezone.utc).isoformat(),
            "publication_enabled":False}

@app.get("/api/status")
def status():
    return {"service":"wero1divulgacao","mode":"staging",
            "publication_enabled":False,"paid_ads_enabled":False,
            "integrations":"not_configured","campaigns_published":0,
            "planner":"available","intent_ranking":"available",
            "happy_path_simulator":"available",
            "note":"Signals require authorized sources; no autonomous publishing."}

@app.post("/api/plan")
def create_plan(payload:PlanRequest):
    offers=[Offer(**o.model_dump()) for o in payload.offers]
    tasks=plan(offers,campaign=payload.campaign,limit=payload.limit)
    return {"mode":"staging","tasks":tasks,"task_count":len(tasks),
            "published":0,"financial_confirmations":0}

@app.post("/api/intent/rank")
def rank_intent(payload:IntentRequest):
    offers=[Offer(**o.model_dump()) for o in payload.offers]
    results=rank_offers(offers,payload.public_queries,payload.trending_topics,payload.limit)
    return {"mode":"staging","ranked_offers":results,"count":len(results),
            "signals_source":"caller_supplied","published":0}

@app.get("/api/simulate/happy-path")
def happy_path():
    """Simulation only: never publishes, charges, pays or writes to production."""
    return simulate_happy_path()
