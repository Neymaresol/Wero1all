from wero1divulgacao.planner import Offer
from wero1divulgacao.intent import rank_offers

def test_public_intent_ranks_authorized_only():
    offers=[Offer(10,"Fone Bluetooth",True,True,True),
            Offer(11,"Fone Bluetooth",False,True,True),
            Offer(12,"Malas de viagem",True,True,True)]
    result=rank_offers(offers,["fone bluetooth barato"],["fone bluetooth"],10)
    assert [r["offer_id"] for r in result]==[10,12]
    assert result[0]["tag1_score"]>0 and result[0]["tag2_score"]>0
