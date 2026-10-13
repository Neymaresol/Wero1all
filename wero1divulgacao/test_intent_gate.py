from wero1divulgacao.planner import Offer
from wero1divulgacao.intent import rank_offers

def test_only_authorized_with_positive_interest():
    offers = [Offer(1, "Batom vermelho", True, True, True),
              Offer(2, "Banana", True, True, True),
              Offer(3, "Batom vermelho", False, True, True)]
    result = rank_offers(offers, ["batom vermelho"], [], limit=10)
    assert [r["offer_id"] for r in result] == [1]
    assert result[0]["tag1_score"] > 0

def test_accent_normalization_and_no_signals():
    offers = [Offer(4, "Maquiagem para lábios", True, True, True)]
    assert rank_offers(offers, ["labios"], [], 10)[0]["offer_id"] == 4
    assert rank_offers(offers, [], [], 10) == []

def test_invalid_ids_and_limits():
    assert rank_offers([Offer(0, "Batom", True, True, True)], ["batom"], [], 10) == []
    try:
        rank_offers([], [], [], 1001)
        assert False
    except ValueError:
        pass
