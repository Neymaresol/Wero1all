from fastapi import FastAPI
from pydantic import BaseModel, Field
from datetime import datetime, timezone
from typing import List
from wero1divulgacao.planner import Offer, plan

app = FastAPI(title="Wero1Divulgacao", version="0.2.0-dev")

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

@app.get("/health")
def health():
    return {"status": "ok", "service": "wero1divulgacao", "version": "0.2.0-dev",
            "mode": "staging", "time": datetime.now(timezone.utc).isoformat(),
            "publication_enabled": False}

@app.get("/api/status")
def status():
    return {"service": "wero1divulgacao", "mode": "staging",
            "publication_enabled": False, "paid_ads_enabled": False,
            "integrations": "not_configured", "campaigns_published": 0,
            "planner": "available", "note": "No automated publications or verified sales."}

@app.post("/api/plan")
def create_plan(payload: PlanRequest):
    """Planning only. Does not publish, write to DB or create sales."""
    offers = [Offer(**o.model_dump()) for o in payload.offers]
    tasks = plan(offers, campaign=payload.campaign, limit=payload.limit)
    return {"mode": "staging", "tasks": tasks, "task_count": len(tasks),
            "published": 0, "financial_confirmations": 0}
