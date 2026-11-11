from wero1divulgacao.planner import Offer, plan
def test_only_authorized():
    items=[Offer(1,"ok",True,True,True),Offer(2,"no",False,True,True)]
    result=plan(items,campaign="launch",limit=100)
    assert len(result)==6
    assert all(x["offer_id"]==1 and not x["published"] for x in result)
def test_limit_and_trace():
    result=plan([Offer(1,"ok",True,True,True)],campaign="launch",limit=2)
    # task_id remains in task metadata; Wero1Mercados persists campaign only.
    assert len(result) == 2
    assert all(x["task_id"].startswith("launch:1:") for x in result)
    assert all("campaign=" in x["url"] for x in result)
    assert len({x["tracking_campaign"] for x in result}) == 2
def test_reject_overflow():
    try:
        plan([],campaign="launch",limit=1001)
        assert False
    except ValueError:
        pass
