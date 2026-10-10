"""Safe commercial worker foundation: builds plans, never publishes without an authorized adapter.

The module is intentionally not wired into application startup. It can be tested
without creating clicks, conversions, or external network activity.
"""
from dataclasses import dataclass
from datetime import datetime, timezone
from urllib.parse import urlencode

@dataclass(frozen=True)
class CampaignTask:
    task_id: str
    offer_id: int
    channel: str
    tracked_path: str
    status: str = "AWAITING_AUTHORIZED_PUBLISHER"

def plan_campaigns(offers, *, channels=("owned_site",), max_tasks=30):
    """Only active offers with valid integer IDs. Deterministic task identifiers."""
    tasks = []
    seen = set()
    for offer in offers:
        if not offer.get("active", False):
            continue
        try:
            offer_id = int(offer["id"])
            if offer_id <= 0:
                continue
        except (KeyError, ValueError, TypeError):
            continue
        for channel in channels:
            if channel not in {"owned_site", "approved_social"}:
                continue
            key = (offer_id, channel)
            if key in seen:
                continue
            seen.add(key)
            path = "/go/" + str(offer_id) + "?" + urlencode({"channel":channel,"campaign":"paradigma-worker"})
            tasks.append(CampaignTask("offer-%s-%s" % key, offer_id, channel, path))
            if len(tasks) >= max_tasks:
                return tasks
    return tasks

def report(tasks):
    return {"generated_at":datetime.now(timezone.utc).isoformat(),
            "planned":len(tasks),"published":0,"confirmed_sales":None,
            "tasks":[task.__dict__ for task in tasks],
            "note":"Planning is not publication, traffic, or sales."}
