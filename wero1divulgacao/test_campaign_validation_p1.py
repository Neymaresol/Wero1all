"""Offline P1 attribution-contract checks: no HTTP, database or publication I/O."""
from urllib.parse import parse_qs, urlparse

import pytest

from wero1divulgacao.planner import Offer, plan


def test_planner_rejects_campaign_labels_backend_would_silently_discard():
    offer = Offer(7, "Curso autorizado", True, True, True)
    for invalid in ("", "a" * 81, "ação", "campanha espaço", "a/b"):
        with pytest.raises(ValueError, match="invalid campaign"):
            plan([offer], campaign=invalid)


def test_planner_preserves_bounded_ascii_campaign_for_tracking():
    offer = Offer(7, "Curso autorizado", True, True, True)
    campaign = "c" * 80
    tasks = plan([offer], campaign=campaign, channels=("facebook",),
                 tags=("tag1_search",), limit=1)
    assert len(tasks) == 1
    query = parse_qs(urlparse(tasks[0]["url"]).query)
    assert query["campaign"] == [tasks[0]["tracking_campaign"]]
    assert tasks[0]["parent"] == campaign
    assert len(tasks[0]["tracking_campaign"]) == 80
    assert tasks[0]["tracking_campaign"].isascii()
    assert query["channel"] == ["facebook"]
    assert tasks[0]["state"] == "proposed"
    assert tasks[0]["published"] is False
    assert tasks[0]["sales_confirmed"] is None


def test_campaign_label_is_not_authentication_or_publication_evidence():
    task = plan([Offer(1, "Curso", True, True, True)], campaign="fb-20261029", limit=1)[0]
    assert task["url"].startswith("https://wero1mercados.onrender.com/go/1?")
    assert task["clicks"] is None
    assert task["sales_confirmed"] is None
    assert task["published"] is False
