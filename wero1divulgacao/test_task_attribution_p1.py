"""Offline campaign attribution contract; no HTTP, DB or publication I/O."""
from urllib.parse import parse_qs, urlparse

from wero1divulgacao.planner import Offer, plan


def _query(task):
    return parse_qs(urlparse(task["url"]).query)


def test_every_planned_offer_tag_channel_gets_distinct_persistable_campaign():
    offers = [
        Offer(7, "Curso A", True, True, True),
        Offer(8, "Curso B", True, True, True),
    ]
    tasks = plan(
        offers, campaign="fb-organico-20261029",
        channels=("facebook", "instagram"), limit=8,
    )
    assert len(tasks) == 8
    labels = [task["tracking_campaign"] for task in tasks]
    assert len(set(labels)) == 8
    for task in tasks:
        query = _query(task)
        assert set(query) == {"channel", "campaign"}
        assert query["channel"] == [task["channel"]]
        assert query["campaign"] == [task["tracking_campaign"]]
        assert 1 <= len(task["tracking_campaign"]) <= 80
        assert all(c.isascii() and (c.isalnum() or c in "-_") for c in task["tracking_campaign"])
        assert task["parent"] == "fb-organico-20261029"
        assert task["state"] == "proposed"
        assert task["published"] is False
        assert task["clicks"] is None
        assert task["sales_confirmed"] is None
    assert labels == [t["tracking_campaign"] for t in plan(
        offers, campaign="fb-organico-20261029",
        channels=("facebook", "instagram"), limit=8,
    )]


def test_long_campaigns_do_not_collide_after_prefix_truncation():
    base = "c" * 79
    offers = [Offer(1, "A", True, True, True)]
    first = plan(offers, campaign=base + "x", limit=1)[0]
    second = plan(offers, campaign=base + "y", limit=1)[0]
    assert first["tracking_campaign"] != second["tracking_campaign"]
    assert len(first["tracking_campaign"]) == 80
    assert len(second["tracking_campaign"]) == 80


def test_unapproved_offer_never_creates_trackable_task():
    tasks = plan([
        Offer(1, "No affiliate authorization", True, True, False),
        Offer(2, "Inactive", True, False, True),
    ], campaign="organic", limit=5)
    assert tasks == []
