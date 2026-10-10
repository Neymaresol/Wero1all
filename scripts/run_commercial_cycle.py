"""One-shot commercial worker: real API reads, authenticated heartbeat, no synthetic sales.

Run from an external scheduler only after durable storage and permissions are checked.
Environment: WERO_BASE_URL, WERO_ADMIN_TOKEN, WERO_ROBOT_ID.
No publication is performed without an approved publisher integration.
"""
import json
import os
import sys
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit

from commercial_worker import plan_campaigns, report

def api(base, path, *, token=None, payload=None):
    url = base.rstrip("/") + path
    data = json.dumps(payload).encode() if payload is not None else None
    headers = {"Accept":"application/json"}
    if data is not None:
        headers["Content-Type"] = "application/json"
    if token:
        headers["Authorization"] = "Bearer " + token
    with urlopen(Request(url, data=data, headers=headers), timeout=15) as response:
        return json.load(response)

def run():
    base = os.environ.get("WERO_BASE_URL", "").rstrip("/")
    token = os.environ.get("WERO_ADMIN_TOKEN", "")
    robot = os.environ.get("WERO_ROBOT_ID", "WERO1-WORKER")
    parsed = urlsplit(base)
    if parsed.scheme != "https" or not parsed.netloc or parsed.username or parsed.password:
        raise ValueError("WERO_BASE_URL must be an HTTPS URL without credentials")
    if not token:
        raise ValueError("WERO_ADMIN_TOKEN is required")
    if not robot or len(robot)>80:
        raise ValueError("Invalid WERO_ROBOT_ID")
    acquisition = api(base, "/api/acquisition")
    queue = acquisition.get("campaign_queue", [])
    # Planning requires no external publication and creates no artificial clicks.
    offers = [{"id": item.get("offer_id"), "active": True} for item in queue]
    tasks = plan_campaigns(offers, channels=("owned_site",), max_tasks=30)
    heartbeat = api(base, "/api/robots/heartbeat", token=token,
                    payload={"robot_id": robot, "parent_robot_id": "WERO1-PAI"})
    if not heartbeat.get("accepted"):
        raise RuntimeError("Heartbeat not accepted")
    result = report(tasks)
    result.update({"robot_id":robot, "heartbeat_accepted":True,
                   "acquisition_bottleneck":acquisition.get("bottleneck"),
                   "planning_cycle_verified":True,
                   "publication_verified":False,
                   "note":"Worker API cycle completed; no campaigns published or sales claimed."})
    print(json.dumps(result, ensure_ascii=False))
    return 0

if __name__ == "__main__":
    try:
        sys.exit(run())
    except (ValueError, RuntimeError, HTTPError, URLError, TimeoutError) as exc:
        print(json.dumps({"status":"error","error_type":type(exc).__name__,
                          "message":str(exc)[:240]}), file=sys.stderr)
        sys.exit(1)
