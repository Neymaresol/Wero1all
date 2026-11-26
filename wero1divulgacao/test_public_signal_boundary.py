"""Offline P1 regression: public intent is advisory, never authenticated conversion evidence.

No HTTP calls, external integrations, database writes, or commercial events.
"""
import ast
from pathlib import Path

from wero1divulgacao.intent import rank_offers
from wero1divulgacao.planner import Offer, plan


def test_zero_intent_and_unapproved_offers_cannot_enter_ranked_candidates():
    offers = [
        Offer(1, "Fone bluetooth", True, True, True),
        Offer(2, "Fone bluetooth", False, True, True),
        Offer(3, "Batom vermelho", True, True, True),
    ]
    assert rank_offers(offers, [], [], 10) == []
    assert [row["offer_id"] for row in rank_offers(offers, ["fone bluetooth"], [], 10)] == [1]


def test_public_signal_api_marks_source_as_caller_supplied_and_publishes_nothing():
    source = (Path(__file__).resolve().parent / "app.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    route = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "rank_intent")
    returns = [n.value for n in route.body if isinstance(n, ast.Return)]
    assert len(returns) == 1 and isinstance(returns[0], ast.Dict)
    fields = {
        key.value: value
        for key, value in zip(returns[0].keys, returns[0].values)
        if isinstance(key, ast.Constant) and isinstance(key.value, str)
    }
    assert isinstance(fields["signals_source"], ast.Constant)
    assert fields["signals_source"].value == "caller_supplied"
    assert isinstance(fields["published"], ast.Constant)
    assert fields["published"].value == 0


def test_planner_creates_proposals_not_published_ads_or_confirmed_sales():
    tasks = plan([Offer(5, "Curso de Python", True, True, True)],
                 campaign="offline_provenance_check", limit=1)
    assert len(tasks) == 1
    task = tasks[0]
    assert task["state"] == "proposed"
    assert task["published"] is False
    assert task["sales_confirmed"] is None
    assert "/go/5?" in task["url"]
    assert "/out/" not in task["url"]
