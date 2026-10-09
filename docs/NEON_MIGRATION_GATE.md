# Wero1 Operario — Neon PostgreSQL migration gate
# 2026-10-09 — STAGING ONLY, no production switch
#
# Neon project: tiny-bread-08131973
# Database: wero1_operario
# Existing Render SQLite DB: /app/data/wero1.db
#
# Before any cutover:
# 1. Capture a consistent snapshot of the CURRENT SQLite DB from the live Render instance.
#    Do not assume prior click records survived previous redeploys.
# 2. Compare all table counts, offers IDs and HotLinks, transactions and event IDs.
# 3. Ensure event/webhook deduplication, financial reversals and historical IDs survive.
# 4. Adapt ALL app SQL (SQLite '?' params, INSERT OR IGNORE, MAX() scalar,
#    AUTOINCREMENT, boolean flags, row_factory, lastrowid) for psycopg.
# 5. Ensure /go/{offer_id} commits tracked click BEFORE redirect.
# 6. Ensure webhooks write atomically and deduplicate transaction/event IDs.
# 7. Add a robot registry and authenticated heartbeat. Registration alone
#    MUST NOT imply a running worker.
# 8. Validate /health, /api/status, /api/attribution, /api/commercial,
#    /api/offers and /api/growth on a staging deployment.
# 9. Cut over only after explicit parity checks, health checks, canary
#    and documented rollback. Keep the existing production version online.
#
# SECURITY: DATABASE_URL must be configured as a secret in Render;
# never commit credentials to GitHub.
# COST: Neon free plan has limits. Upgrade only with user's approval.
