from fastapi.testclient import TestClient

from wero1divulgacao.app import app


def test_caller_supplied_offer_flags_cannot_create_campaign_tasks():
    client = TestClient(app)
    response = client.post(
        "/api/plan",
        json={
            "campaign": "organic-test",
            "offers": [
                {
                    "id": 71,
                    "title": "Oferta declarada pelo solicitante",
                    "approved": True,
                    "active": True,
                    "affiliate_authorized": True,
                }
            ],
            "limit": 10,
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["tasks"] == []
    assert payload["task_count"] == 0
    assert payload["planning_status"] == "BLOCKED_NO_AUTHORIZED_CATALOG_SOURCE"
    assert payload["source"] == "caller_supplied_unverified"
    assert payload["candidate_offers_received"] == 1
    assert payload["published"] == 0
    assert payload["financial_confirmations"] == 0
    assert payload["publication_allowed"] is False
    assert payload["requires_manual_review"] is True


def test_status_reports_catalog_planner_blocked_without_server_side_source():
    client = TestClient(app)
    response = client.get("/api/status")

    assert response.status_code == 200
    payload = response.json()
    assert payload["planner"] == "BLOCKED_NO_AUTHORIZED_CATALOG_SOURCE"
    assert payload["catalog_planning_status"] == "BLOCKED_NO_AUTHORIZED_CATALOG_SOURCE"
    assert payload["integrations"] == "not_configured"
    assert payload["publication_enabled"] is False
    assert payload["paid_ads_enabled"] is False
    assert payload["campaigns_published"] == 0
