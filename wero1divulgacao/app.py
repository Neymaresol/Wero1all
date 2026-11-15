from fastapi import FastAPI
from pydantic import BaseModel, Field
from datetime import datetime, timezone
from typing import List
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
            "integrations":"not_configured",
            "planner":"BLOCKED_NO_AUTHORIZED_CATALOG_SOURCE",
            "catalog_planning_status":"BLOCKED_NO_AUTHORIZED_CATALOG_SOURCE",
            "campaigns_published":0,
            "intent_ranking_endpoint":"available",
            "intent_ranking":"BLOCKED_NO_AUTHORIZED_SIGNAL_SOURCE",
            "intent_ranking_status":"BLOCKED_NO_AUTHORIZED_SIGNAL_SOURCE",
            "happy_path_simulator":"available",
            "note":"Planning and intent ranking remain blocked until server-side authorized catalog and signal sources are verified; caller-supplied offer flags are not authorization and no autonomous publishing is enabled."}

@app.post("/api/plan")
def create_plan(payload:PlanRequest):
    # Request-body flags are caller-controlled and cannot prove catalog approval,
    # partner authorization, availability, price, or source freshness.
    # Keep the endpoint explicit and fail-closed until a server-side catalog
    # adapter validates those facts against an authorized provider.
    return {
        "mode":"staging",
        "tasks":[],
        "task_count":0,
        "planning_status":"BLOCKED_NO_AUTHORIZED_CATALOG_SOURCE",
        "source":"caller_supplied_unverified",
        "candidate_offers_received":len(payload.offers),
        "published":0,
        "financial_confirmations":0,
        "publication_allowed":False,
        "requires_manual_review":True,
    }

@app.post("/api/intent/rank")
def rank_intent(payload:IntentRequest):
    # public_queries and trending_topics are caller-supplied request data,
    # not independently authenticated signals from an approved provider.
    # Fail closed until a server-side source adapter verifies provenance,
    # collection time, source identity and integrity.
    return {
        "mode":"staging",
        "ranked_offers":[],
        "count":0,
        "signals_source":"caller_supplied_unverified",
        "ranking_status":"BLOCKED_NO_AUTHORIZED_SIGNAL_SOURCE",
        "candidate_offers_received":len(payload.offers),
        "published":0,
        "publication_allowed":False,
        "requires_manual_review":True,
    }

@app.get("/api/simulate/happy-path")
def happy_path():
    """Simulation only: never publishes, charges, pays or writes to production."""
    return simulate_happy_path()
