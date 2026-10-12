"""Read-only reconciliation of SQLite operational data against Neon.

No automatic copy, bootstrap, activation or financial reconciliation is performed.
Run against a SQLite snapshot and a Neon connection with SELECT-only permissions.
"""
import os
import sqlite3
from pathlib import Path

TABLES = ("offers", "catalog_products", "campaign_clicks", "transactions", "events", "robot_heartbeats")

def sqlite_inventory(path):
    """Never create an absent SQLite database as a side effect of auditing."""
    p = Path(path)
    if not p.is_file():
        raise FileNotFoundError(f"SQLite source does not exist: {p}")
    with sqlite3.connect(f"file:{p.resolve()}?mode=ro", uri=True) as db:
        available = {row[0] for row in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        return {name: db.execute(f'SELECT COUNT(*) FROM "{name}"').fetchone()[0]
                if name in available else None for name in TABLES}

def neon_inventory(connection):
    """Use an existing read-only psycopg connection, without schema mutations."""
    with connection.cursor() as cur:
        cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
        available = {r[0] for r in cur.fetchall()}
        result = {}
        for name in TABLES:
            if name not in available:
                result[name] = None
            else:
                cur.execute(f'SELECT COUNT(*) FROM public."{name}"')
                result[name] = cur.fetchone()[0]
        return result

def compare(local, remote):
    return {name: {"sqlite": local.get(name), "neon": remote.get(name),
                   "match": local.get(name) is not None and remote.get(name) is not None
                            and local[name] == remote[name]}
            for name in TABLES}

def main():
    import json
    path = os.environ.get("DB_PATH", "/app/data/wero1.db")
    url = os.environ.get("DATABASE_URL")
    if not url:
        raise SystemExit("DATABASE_URL required (use a SELECT-only database role)")
    import psycopg
    local = sqlite_inventory(path)
    with psycopg.connect(url, options="-c default_transaction_read_only=on") as conn:
        remote = neon_inventory(conn)
    print(json.dumps({"sqlite_path": str(Path(path).resolve()),
                      "tables": compare(local, remote),
                      "warning": "Counts alone do not prove row-level parity or verified sales."}, indent=2))

if __name__ == "__main__":
    main()
