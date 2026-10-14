"""Regressoes P0 do ranking INT.1/INT.2 (somente staging, sem publicacao)."""
from wero1divulgacao.intent import rank_offers
from wero1divulgacao.planner import Offer


def test_zero_interest_never_enters_ranking():
    offers = [
        Offer(101, "Fone Bluetooth", True, True, True),
        Offer(102, "Malas de viagem", True, True, True),
    ]
    ranked = rank_offers(offers, ["fone bluetooth barato"], ["fone bluetooth"])
    assert [item["offer_id"] for item in ranked] == [101]
    assert all(item["total_score"] > 0 for item in ranked)


def test_int1_or_int2_alone_can_qualify():
    offers = [
        Offer(201, "Notebook", True, True, True),
        Offer(202, "Malas", True, True, True),
    ]
    ranked = rank_offers(offers, ["notebook"], ["malas"])
    assert {item["offer_id"] for item in ranked} == {201, 202}
    assert next(item for item in ranked if item["offer_id"] == 201)["tag2_score"] == 0
    assert next(item for item in ranked if item["offer_id"] == 202)["tag1_score"] == 0


def test_authorization_and_valid_id_are_mandatory():
    offers = [
        Offer(301, "Notebook", False, True, True),
        Offer(302, "Notebook", True, False, True),
        Offer(303, "Notebook", True, True, False),
        Offer(0, "Notebook", True, True, True),
        Offer(304, "Notebook", True, True, True),
    ]
    ranked = rank_offers(offers, ["notebook"], [])
    assert [item["offer_id"] for item in ranked] == [304]


def test_empty_signals_return_no_ranked_offers():
    offers = [Offer(401, "Notebook", True, True, True)]
    assert rank_offers(offers, [], []) == []
