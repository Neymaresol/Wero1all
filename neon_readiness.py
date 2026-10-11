"""Read-only Neon readiness checks. Does not migrate or mutate commercial records."""
import os
from datetime import datetime, timezone, timedelta
from urllib.parse import urlparse

TABLES = ("offers", "catalog_products", "campaign_clicks", "transactions", "robot_registry")

def neon_readiness(connect=None, dsn=None):
    dsn = dsn if dsn is not None else os.getenv("DATABASE_URL", "")
    if not dsn:
        return {"configured": False, "connected": False, "ready_for_cutover": False,
                "reason": "DATABASE_URL missing; existing SQLite remains authoritative"}
    parsed = urlparse(dsn)
    if parsed.scheme not in ("postgres", "postgresql") or not parsed.hostname:
        return {"configured": True, "connected": False, "ready_for_cutover": False,
                "reason": "invalid PostgreSQL connection URL"}
    if connect is None:
        import psycopg
        connect = psycopg.connect
    try:
        with connect(dsn, connect_timeout=5) as conn:
            with conn.cursor() as cur:
                cur.execute("BEGIN READ ONLY")
                cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
                found = {r[0] for r in cur.fetchall()}
                missing = sorted(set(TABLES) - found)
                counts = {}
                if not missing:
                    for table in TABLES:
                        cur.execute("SELECT COUNT(*) FROM " + table)
                        counts[table] = int(cur.fetchone()[0])
                    cur.execute("SELECT robot_id, operational_status, last_heartbeat FROM robot_registry ORDER BY robot_id LIMIT 100")
                    robots = []
                    cutoff = datetime.now(timezone.utc) - timedelta(seconds=180)
                    for robot_id, status, heartbeat in cur.fetchall():
                        fresh = bool(heartbeat and heartbeat.astimezone(timezone.utc) >= cutoff)
                        robots.append({"robot_id": robot_id, "status": status, "heartbeat_fresh": fresh})
                else:
                    robots = []
                conn.rollback()
        return {"configured": True, "connected": True, "schema_complete": not missing,
                "missing_tables": missing, "counts": counts, "robots": robots,
                "ready_for_cutover": False,
                "reason": "Read-only inspection only; migration, parity and rollback validation required"}
    except Exception as exc:
        return {"configured": True, "connected": False, "ready_for_cutover": False,
                "reason": "connection/query failed", "error_type": type(exc).__name__}
