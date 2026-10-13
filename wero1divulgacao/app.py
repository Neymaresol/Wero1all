from fastapi import FastAPI
from datetime import datetime, timezone

app = FastAPI(title="Wero1Divulgacao", version="0.1.0-dev")

@app.get("/health")
def health():
    return {"status": "ok", "service": "wero1divulgacao", "version": "0.1.0-dev", "mode": "staging", "time": datetime.now(timezone.utc).isoformat(), "publication_enabled": False}

@app.get("/api/status")
def status():
    return {"service": "wero1divulgacao", "mode": "staging", "publication_enabled": False, "paid_ads_enabled": False, "integrations": "not_configured", "campaigns_published": 0, "note": "Bootstrap only; no automated publications or verified metrics."}
