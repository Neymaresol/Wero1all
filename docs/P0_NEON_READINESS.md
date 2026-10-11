# GAP P0 — Neon readiness (11/10/2026)
This change adds **read-only** Neon diagnostics; it intentionally does not switch production from SQLite to Neon.
The existing main.py uses SQLite-specific SQL (PRAGMA, INSERT OR IGNORE, ? placeholders, lastrowid, AUTOINCREMENT). Replacing DB_PATH with DATABASE_URL without porting those statements would break sales and heartbeat endpoints.

Run: `python -m unittest discover -s tests -p 'test_neon_readiness.py'`

Before cutover:
1. Confirm which SQLite volume is actually authoritative; back up with checksum.
2. Align Neon schema, including robot_heartbeats vs robot_registry; never infer heartbeat from an empty field.
3. Port every SQL operation to PostgreSQL and run integration tests against an isolated Neon branch.
4. Migrate offers, click events, transaction ledger and heartbeat rows idempotently; compare totals and checksums.
5. Validate provider-sourced confirmed sales, redirects, admin auth, rollback, and canary.
6. Only then propose a separately approved deployment. No production changes in this PR.
