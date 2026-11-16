"""Regression tests for the deployed fail-closed Wero1Divulgacao API.

These tests call only pure request handlers. They do not access a database,
invoke provider APIs, publish posts, create clicks, or record conversions.
"""
from wero1divulgacao.app import (
    IntentRequest,
    OfferInput,
    PlanRequest,
    create_plan,
    rank_intent,
)


def test_plan_does_not_trust_caller_supplied_offer_flags():
    payload = PlanRequest(
        campaign="regression-only",
        offers=[
            OfferInput(
                id=101,
                title="Curso de Python",
                approved=True,
                active=True,
                affiliate_authorized=True,
            )
        ],
        limit=10,
    )

    result = create_plan(payload)

    assert result["tasks"] == []
    assert result["task_count"] == 0
    assert result["planning_status"] == "BLOCKED_NO_AUTHORIZED_CATALOG_SOURCE"
    assert result["source"] == "caller_supplied_unverified"
    assert result["published"] == 0
    assert result["financial_confirmations"] == 0
    assert result["publication_allowed"] is False


def test_rank_does_not_trust_caller_supplied_tag1_and_tag2():
    payload = IntentRequest(
        offers=[
            OfferInput(
                id=102,
                title="Curso de Python",
                approved=True,
                active=True,
                affiliate_authorized=True,
            )
        ],
        public_queries=["curso python"],
        trending_topics=["curso python"],
        limit=10,
    )

    result = rank_intent(payload)

    assert result["ranked_offers"] == []
    assert result["count"] == 0
    assert result["ranking_status"] == "BLOCKED_NO_AUTHORIZED_SIGNAL_SOURCE"
    assert result["signals_source"] == "caller_supplied_unverified"
    assert result["published"] == 0
    assert result["publication_allowed"] is False
