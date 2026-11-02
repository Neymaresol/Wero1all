from wero1divulgacao.planner import Offer
from wero1divulgacao.intent import rank_offers


def test_only_authorized_with_positive_interest_in_both_sources():
    offers = [
        Offer(1, "Batom vermelho", True, True, True),
        Offer(2, "Banana", True, True, True),
        Offer(3, "Batom vermelho", False, True, True),
    ]
    result = rank_offers(
        offers, ["batom vermelho"], ["batom vermelho"], limit=10
    )
    assert [r["offer_id"] for r in result] == [1]
    assert result[0]["tag1_score"] > 0
    assert result[0]["tag2_score"] > 0


def test_zero_in_either_score_excludes_offer():
    offers = [Offer(4, "Curso de Python", True, True, True)]
    assert rank_offers(offers, ["curso python"], [], 10) == []
    assert rank_offers(offers, [], ["curso python"], 10) == []
    result = rank_offers(
        offers, ["curso python"], ["curso python"], 10
    )
    assert len(result) == 1
    assert result[0]["tag1_score"] > 0
    assert result[0]["tag2_score"] > 0


def test_accent_normalization_and_no_signals():
    offers = [Offer(5, "Maquiagem para lábios", True, True, True)]
    result = rank_offers(offers, ["labios"], ["lábios"], 10)
    assert [r["offer_id"] for r in result] == [5]
    assert rank_offers(offers, [], [], 10) == []


def test_invalid_ids_and_limits():
    assert rank_offers(
        [Offer(0, "Batom", True, True, True)], ["batom"], ["batom"], 10
    ) == []
    try:
        rank_offers([], [], [], 1001)
        assert False
    except ValueError:
        pass


def test_unapproved_or_unauthorized_offers_remain_excluded():
    offers = [
        Offer(6, "Curso de Python", False, True, True),
        Offer(7, "Curso de Python", True, True, False),
        Offer(8, "Curso de Python", True, False, True),
    ]
    assert rank_offers(
        offers, ["curso python"], ["curso python"], 10
    ) == []
