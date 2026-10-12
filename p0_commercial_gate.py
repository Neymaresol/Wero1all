"""Read-only commercial readiness checks. Never copies or fabricates source data."""
from datetime import datetime, timezone, timedelta

def readiness(sqlite_counts, neon_counts, heartbeat=None, now=None):
    names = ("offers", "catalog_products", "campaign_clicks", "transactions")
    differences = {name: {"sqlite": sqlite_counts.get(name), "neon": neon_counts.get(name)}
                   for name in names if sqlite_counts.get(name) != neon_counts.get(name)
                   or sqlite_counts.get(name) is None or neon_counts.get(name) is None}
    now = now or datetime.now(timezone.utc)
    fresh = False
    if heartbeat:
        try:
            seen = datetime.fromisoformat(heartbeat.replace("Z", "+00:00"))
            fresh = seen.tzinfo is not None and timedelta(0) <= now - seen <= timedelta(seconds=180)
        except (ValueError, TypeError):
            pass
    return {"ready": not differences and fresh and neon_counts.get("offers", 0) > 0,
            "differences": differences, "heartbeat_fresh": fresh,
            "sales_confirmed": None, "commission_confirmed": None,
            "note": "Inventory parity is not data equivalence; manual record-level double-check required."}
