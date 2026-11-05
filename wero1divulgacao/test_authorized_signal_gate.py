from fastapi.testclient import TestClient

from wero1divulgacao.app import app


def test_caller_supplied_queries_cannot_unlock_intent_ranking():
    client = TestClient(app)
    response = client.post(
        "/api/intent/rank",
        json={
            "offers": [
                {
                    "id": 1,
                    "title": "Fone Bluetooth",
                    "approved": True,
                    "active": True,
                    "affiliate_authorized": True,
                }
            ],
            "public_queries": ["fone bluetooth comprar"],
            "trending_topics": ["fone bluetooth"],
            "limit": 10,
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["ranked_offers"] == []
    assert payload["count"] == 0
    assert payload["signals_source"] == "caller_supplied_unverified"
    assert payload["ranking_status"] == "BLOCKED_NO_AUTHORIZED_SIGNAL_SOURCE"
    assert payload["publication_allowed"] is False
    assert payload["requires_manual_review"] is True
    assert payload["published"] == 0


def test_status_does_not_advertise_blocked_intent_ranking_as_available():
    client = TestClient(app)
    status_response = client.get("/api/status")
    rank_response = client.post(
        "/api/intent/rank",
        json={
            "offers": [],
            "public_queries": ["consulta pública"],
            "trending_topics": ["tendência pública"],
            "limit": 10,
        },
    )

    assert status_response.status_code == 200
    assert rank_response.status_code == 200
    status = status_response.json()
    ranking = rank_response.json()

    assert status["intent_ranking_endpoint"] == "available"
    assert status["intent_ranking"] == "BLOCKED_NO_AUTHORIZED_SIGNAL_SOURCE"
    assert status["intent_ranking_status"] == ranking["ranking_status"]
    assert status["publication_enabled"] is False
    assert status["paid_ads_enabled"] is False
    assert status["integrations"] == "not_configured"
    assert status["campaigns_published"] == 0
