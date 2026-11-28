# PARADIGMA — Iteração 33 (2026-11-28 05:16 BRT)

## Escopo e segurança
Read-only inspection of Render, Neon staging/production, GitHub PRs/CI, and Metricool. One documentation-only commit to this isolated branch. No production/staging deploy, merge, database write, paid ad, post, click, conversion, sale, commission, or payment was created. Wero1Operário and Wero1Elétrico were not touched.

## P0 — Render production
- Wero1Mercados service `srv-db2fvq4s728c73cahjq0`: main branch, Free, auto-deploy enabled, 1 instance, not suspended, Health Check Path empty.
- Render Postgres inventory: none found. Requested database `dpg-db2h93h7lnhs73ev17og-a` is not present in inventory; previous API lookup returned 404.
- The reported Free DB expiry 2026-11-05 is past.
- Last 7-day service-event page returned 20 events, all `server_failed` with exit code 3. Five occurred within the last 24h. Latest event: 2026-11-27 18:54:24 UTC (15:54:24 BRT).
- Latest Render app-log query for 2026-11-28 07:00–08:20 UTC returned no records. This does not prove healthy runtime.
- CPU, memory, HTTP request, latency metrics were not available in the inspected listing.
- Direct HTTP opens of production `/health`, `/ready`, and both staging health endpoints were inaccessible through the available browser tool; runtime HTTP remains unverified.
- Current main SHA: `1b17084ee04c910d19a694bf79dd4f6bb4ea4516`.

## P0 — Neon
**Production**: `wero1mercados-production`, project `long-tooth-35390946`, PG17, AWS us-east-2, default branch Ready, database `neondb`; public tables = 0; snapshots = 0; snapshot schedule empty. Quota reset `2026-12-01T00:00:00Z`.

**Staging**: `wero1mercados-staging`, project `floral-hat-53843763`, PG17, AWS us-east-2; 15 public tables.
- `product_offers`: 19 total, 19 active, 0 available, 0 provider-verified, 0 with positive price/commission, 0 updated in the last 7 days.
- `offers`: 20; partners: 2 (previously confirmed 1 active).
- clicks, conversions, outbound tokens, conversion audits, ledger, catalog visits and landing visits: all 0.
- Latest staging persistence probe readback: `paradigma-auto11-20261128-0011-bst`, 2026-11-28 03:13:44.558 UTC. Purpose is operational persistence only, explicitly no commercial event.
- Staging snapshots/restore proof: none.

## P0 — Code and pull requests
- Main currently excludes zero-click offers from `/api/tags/trends`, but the premium AI ranking query lacks both a positive-click requirement and a 7-day recent-click requirement; offers with no INT.1/INT.2 can still be listed. Main is `1b17084...`.
- PR #137 candidate adds `COUNT(clicks) > 0` and a positive last-7-days click gate to the premium ranking. It also introduces explicit `storage_persistence_status=NOT_VERIFIED`, readiness separation, prefetch guard, and short-lived single-use offer-bound outbound tokens. Tokens/clicks are consultative only and are not INT proof.
- PR #137 head `d49bb705c8500acf4622f209acc5a6ece4328` has **no workflow runs returned**; direct check coverage is missing.
- PR #140 head `05306f2efe9af0d4fb7d147294a5bcce4c574b09`: 4/4 workflows succeeded (campaign, PARADIGMA P0, commercial contract, isolated PG17/18). This stacked PR includes #137 base changes and keeps conversion ingest closed until authenticated partner adapter exists.
- PR #141 head `3187aea0ac32bfb4ce539c4154ddbc9e70dcbb2e`: 4/4 workflows succeeded; Werozinha cards use protected `/go/` route.
- Wero1Divulgação PR #47 head `e4d47ecdf101b3184db8d8660b02bb2de107873c`: 2/2 workflows succeeded; TAG1 and TAG2 must each be positive.
- PR #50 head `b8203686def6e9036a19425f7dec135b0d0cb6f5`: 2/2 workflows succeeded; ranking status explicitly `registered_fail_closed`.
- All listed PRs remain open/Draft; none was merged. CI success on stacked #140/#141 does not replace runtime staging HTTP tests, restore proof, integrated Double Check, or rollback.
- No new code changes were justified this run.

## P1 — Metricool (brand 7259526, America/Sao_Paulo)
- Instagram connected: `@neymaresoloficial`; requested account: `@neymaresol` — mismatch confirmed.
- Facebook and TikTok connected; TikTok handle `@neymaresoltiktok`.
- TikTok posts analytics (21–28 Nov): 25 rows, 677 views, 66 likes, 2 comments, 0 shares; reach field returned no data.
- Instagram evolution: 45 followers in the last returned follower records (latest date 26 Nov); no post/reel interaction metrics returned.
- Facebook post analytics: no rows.
- Scheduled posts for 28 Nov–05 Dec: 0.
- Saturday best-time scores: Facebook 10:00 = 8,850; TikTok 10:00 = 852; Instagram all zero. Scores are relative timing suggestions, not sales forecasts.
- Campaign attribution/SmartLink clicks not available. No post was created or scheduled.

## P1 — public editorial signal
- Senacon/MJSP online-shopping guide published 25 Nov 2026: compare full price incl. freight/fees/interest; check store reputation, official URLs, Pix recipient, avoid fake urgency and retain receipts. https://www.gov.br/secom/pt-br/acompanhe-a-secom/noticias/2026/11/cartilha-do-ministerio-da-justica-e-seguranca-publica-orienta-consumidores-nas-compras-da-black-friday
- Procon-MT warning published 09 Nov: beware suspicious links and false discounts, verify seller/site and Pix/boleto recipient. https://www.secom.mt.gov.br/web/procon/w/procon-mt-alerta-para-golpes-na-black-friday
- Senacon notified platforms/retailers on 18 Nov about safeguards against fraud, misleading advertising, false discounts, sellers/products and refund/return issues. https://www.gov.br/mj/pt-br/assuntos/noticias/senacon-notifica-plataformas-e-varejistas-para-prevenir-problemas-durante-a-black-friday
Editorial idea: short Werozinha content on 4 checks before clicking (price history, full checkout price, seller/URL, payment recipient). These are public safety signals only, not offers, INT, or conversions.

## Promotion gates
1. Recover/migrate production PostgreSQL.
2. Prove isolated backup and restore.
3. Prove Render staging → Neon staging isolation.
4. HTTP test `/health`, `/ready`, `/go/`, `/out/` in staging.
5. Authenticated partner adapter with signature/identity, offer binding, uniqueness and replay controls.
6. Integrated Double Check and rollback proof.
7. Only then consider promotion.

## Financial truth
Confirmed sales = 0; conversions = 0; commission = R$0.00; payments = R$0.00. No estimates presented as confirmed payments.

**Decision: HOLD.** Production is not recoverable/verified, staging runtime is not homologated, and conversion provenance is not authenticated.
