"""One-time, additive SQLite -> Neon migration. Run on a verified SQLite snapshot.
Never executes at application startup; never invents financial events.
Requires DATABASE_URL and SQLITE_SNAPSHOT. Use staging before production.
"""
import os
import sqlite3
import psycopg
from psycopg.rows import dict_row

TABLES = {
    "offers": ("id","provider","product_id","product_name","hotlink","niche","price","commission","currency","active","created_at","updated_at"),
    "campaign_clicks": ("click_id","offer_id","channel","campaign","robot_id","creative","created_at"),
    "transactions": ("transaction_id","provider","robot_id","product_id","event_state","amount","currency","is_test","confirmed","reversed","first_seen","last_seen"),
    "events": ("id","provider","event_id","robot_id","kind","amount","confirmed","created_at"),
    "event_v112": ("event_id","transaction_id","event_type","is_test","received_at"),
    "catalog_products": ("product_id","ucode","name","status","format","source","eligible","last_scan"),
}
BOOL_COLUMNS = {"active","is_test","confirmed","reversed","eligible"}
PK = {"offers":"id","campaign_clicks":"click_id","transactions":"transaction_id","events":"id","event_v112":"event_id","catalog_products":"product_id"}

def migrate():
    source=os.environ["SQLITE_SNAPSHOT"]
    url=os.environ["DATABASE_URL"]
    if not os.path.isfile(source):
        raise RuntimeError("Verified SQLite snapshot required")
    sqlite=sqlite3.connect(f"file:{source}?mode=ro",uri=True)
    sqlite.row_factory=sqlite3.Row
    with psycopg.connect(url,sslmode="require",row_factory=dict_row) as pg:
        with pg.transaction():
            for table, columns in TABLES.items():
                available={r["name"] for r in sqlite.execute(f"PRAGMA table_info({table})")}
                if not available:
                    raise RuntimeError(f"Source table missing: {table}")
                if not set(columns).issubset(available):
                    raise RuntimeError(f"Source columns missing in {table}: {set(columns)-available}")
                rows=sqlite.execute(f"SELECT {','.join(columns)} FROM {table}").fetchall()
                for row in rows:
                    values=[bool(row[col]) if col in BOOL_COLUMNS else row[col] for col in columns]
                    placeholders=",".join(["%s"]*len(columns))
                    fields=",".join(columns)
                    # Never overwrite destination data. Conflicting IDs require manual reconciliation.
                    pg.execute(f"INSERT INTO {table} ({fields}) VALUES ({placeholders}) ON CONFLICT ({PK[table]}) DO NOTHING",values)
                for row in rows:
                    key=row[PK[table]]
                    check=pg.execute(f"SELECT 1 FROM {table} WHERE {PK[table]}=%s",(key,)).fetchone()
                    if not check: raise RuntimeError(f"Missing migrated {table} key {key}")
                target_count=pg.execute(f"SELECT COUNT(*) AS n FROM {table}").fetchone()["n"]
                if target_count < len(rows): raise RuntimeError(f"Destination count lower than source: {table}")
                print(f"{table}: {len(rows)} source rows verified by key; destination has {target_count}")
            for table in ("offers","events"):
                pg.execute(f"SELECT setval(pg_get_serial_sequence('{table}','id'), GREATEST(COALESCE((SELECT MAX(id) FROM {table}),0),1), true)")
        print("Migration transaction committed; verify row content and reports before cutover")
    sqlite.close()

if __name__=="__main__":
    migrate()
