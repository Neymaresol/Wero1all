"""P0 Double Check: HTTP contract in isolated TestClient (no external calls or DB writes)."""
from fastapi.testclient import TestClient
from wero1divulgacao.app import app

client = TestClient(app)

def test_health_and_status_fail_closed():
    health = client.get("/health")
    assert health.status_code == 200
    assert health.json()["mode"] == "staging"
    assert health.json()["publication_enabled"] is False
    status = client.get("/api/status")
    assert status.status_code == 200
    assert status.json()["paid_ads_enabled"] is False
    assert status.json()["publication_enabled"] is False
    assert status.json()["campaigns_published"] == 0
    assert status.json()["integrations"] == "not_configured"

def test_rank_excludes_unapproved_and_zero_interest():
    offers = [
        {"id": 11, "title": "Batom vermelho", "approved": True, "active": True, "affiliate_authorized": True},
        {"id": 12, "title": "Batom vermelho", "approved": False, "active": True, "affiliate_authorized": True},
        {"id": 13, "title": "Banana", "approved": True, "active": True, "affiliate_authorized": True},
        {"id": 14, "title": "Batom vermelho", "approved": True, "active": False, "affiliate_authorized": True},
        {"id": 15, "title": "Batom vermelho", "approved": True, "active": True, "affiliate_authorized": False},
    ]
    response = client.post("/api/intent/rank", json={
        "offers": offers, "public_queries": ["batom vermelho"],
        "trending_topics": ["batom"], "limit": 10})
    assert response.status_code == 200
    data = response.json()
    assert data["mode"] == "staging"
    assert data["published"] == 0
    assert data["signals_source"] == "caller_supplied"
    assert data["count"] == 1
    assert [x["offer_id"] for x in data["ranked_offers"]] == [11]

    empty = client.post("/api/intent/rank", json={
        "offers": offers, "public_queries": [], "trending_topics": [], "limit": 10})
    assert empty.status_code == 200
    assert empty.json()["count"] == 0

def test_plan_does_not_publish_and_filters_authorization():
    response = client.post("/api/plan", json={
        "campaign": "p0-test-only",
        "offers": [
            {"id": 1, "title": "Batom", "approved": True, "active": True, "affiliate_authorized": True},
            {"id": 2, "title": "Banana", "approved": False, "active": True, "affiliate_authorized": True}
        ],
        "limit": 10})
    assert response.status_code == 200
    data = response.json()
    assert data["mode"] == "staging"
    assert data["published"] == 0
    assert data["financial_confirmations"] == 0
    assert data["task_count"] > 0
    assert all(x["offer_id"] == 1 and x["published"] is False and x["state"] == "proposed"
               for x in data["tasks"])
    assert all("/go/1?" in x["url"] for x in data["tasks"])

def test_simulation_never_reports_real_money():
    response = client.get("/api/simulate/happy-path")
    assert response.status_code == 200
    data = response.json()
    assert data["simulation"] is True
    assert data["real_sales_created"] == 0
    assert data["real_transfers_created"] == 0

def test_invalid_inputs_fail_without_side_effects():
    assert client.post("/api/intent/rank", json={"limit": 1001}).status_code == 422
    assert client.post("/api/plan", json={"campaign": "bad campaign!"}).status_code == 400 or client.post("/api/plan", json={"campaign": "bad campaign!"}).status_code == 422
