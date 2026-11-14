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
    assert payload["intent_ranking"] == "BLOCKED_NO_AUTHORIZED_SIGNAL_SOURCE"
    assert payload["intent_ranking_status"] == "BLOCKED_NO_AUTHORIZED_SIGNAL_SOURCE"


def test_caller_supplied_intent_signals_never_create_authenticated_ranking():
    client = TestClient(app)
    response = client.post(
        "/api/intent/rank",
        json={
            "offers": [
                {
                    "id": 72,
                    "title": "Oferta declarada como aprovada pelo solicitante",
                    "approved": True,
                    "active": True,
                    "affiliate_authorized": True,
                }
            ],
            "public_queries": ["busca declarada pelo solicitante"],
            "trending_topics": ["tendencia declarada pelo solicitante"],
            "limit": 10,
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["ranked_offers"] == []
    assert payload["count"] == 0
    assert payload["signals_source"] == "caller_supplied_unverified"
    assert payload["ranking_status"] == "BLOCKED_NO_AUTHORIZED_SIGNAL_SOURCE"
    assert payload["candidate_offers_received"] == 1
    assert payload["published"] == 0
    assert payload["publication_allowed"] is False
    assert payload["requires_manual_review"] is True



def test_zero_or_partial_int_scores_never_enter_ranking_from_request_body():
    client = TestClient(app)
    response = client.post(
        "/api/intent/rank",
        json={
            "offers": [
                {
                    "id": 81,
                    "title": "INT1 e INT2 zerados",
                    "approved": True,
                    "active": True,
                    "affiliate_authorized": True,
                    "int1_score": 0,
                    "int2_score": 0,
                },
                {
                    "id": 82,
                    "title": "INT2 zerado",
                    "approved": True,
                    "active": True,
                    "affiliate_authorized": True,
                    "int1_score": 7,
                    "int2_score": 0,
                },
                {
                    "id": 83,
                    "title": "INT1 zerado",
                    "approved": True,
                    "active": True,
                    "affiliate_authorized": True,
                    "int1_score": 0,
                    "int2_score": 7,
                },
            ],
            "public_queries": ["sinal informado pelo solicitante"],
            "trending_topics": ["tendencia informada pelo solicitante"],
            "limit": 10,
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["ranked_offers"] == []
    assert payload["count"] == 0
    assert payload["signals_source"] == "caller_supplied_unverified"
    assert payload["ranking_status"] == "BLOCKED_NO_AUTHORIZED_SIGNAL_SOURCE"
    assert payload["candidate_offers_received"] == 3
    assert payload["published"] == 0
    assert payload["publication_allowed"] is False
    assert payload["requires_manual_review"] is True
