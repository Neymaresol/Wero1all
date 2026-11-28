# PARADIGMA — Iteração 12 (28/11/2026 07:18 BRT)

## Decisão
**HOLD — produção não liberada.** Auditoria read-only de Render, GitHub, Neon e Metricool. Única escrita desta rodada: este documento na branch isolada da PR #51. Sem deploy, merge, publicações, cliques, conversões, vendas, comissões ou pagamentos sintéticos. Wero1Operário e Wero1Elétrico não foram alterados.

## P0 — Render produção
- Workspace: My Workspace.
- Serviço Wero1Mercados `srv-db2fvq4s728c73cahjq0`: `main`, Free, autoDeploy ligado, 1 instância, não suspenso, Health Check Path vazio, Oregon.
- PostgreSQL Render: nenhum instance listado; ID antigo `dpg-db2h93h7lnhs73ev17og-a` não encontrado. Expiração informada 2026-11-05 ultrapassada.
- Último deploy Live: 23/10/2026, commit `80018a1c3b4a41d8bb052ddf798b11b10d613afa`.
- Eventos: 20 `server_failed` na página dos últimos 7 dias, todos exit code 3; cursor indica que a página não é a contagem total. 5 eventos nas últimas 24h, 27/11 18:44–18:54 UTC.
- Log mais recente: startup chama `init_db()`, falha de DNS ao resolver hostname PostgreSQL antigo, seguida de `Application startup failed`.
- Métricas de CPU, memória, instâncias, HTTP request count e latência: sem séries nas últimas 24h.
- Tentativas de abrir `/health` de produção e staging pelo navegador falharam; não há confirmação HTTP de health.

## Render staging — deploys confirmados
**Wero1Mercados staging**
- Serviço `srv-db6k648473hc73dkvk70`, branch `dev/p0-provider-reconciliation-20261012`, auto-deploy off, Health Check Path vazio.
- Último deploy Live: 13/10/2026, commit `9a3741d30f18d172b2cacc147427b686100694a4`, versão antiga de vitrine social com links Amazon.
- Eventos e app logs da janela consultada: vazios.
- Código do deploy antigo: `/go/{offer_id}` registra visita no GET e `/out/{offer_id}` registra clique diretamente; não é a candidata P0 atual.

**Wero1Divulgação staging**
- Serviço `srv-db79kdm7bikc73a1rv20`, branch `feat/wero1divulgacao-bootstrap`, auto-deploy off, Health Check Path vazio.
- Último deploy Live: 25/11/2026 05:24:58 UTC, commit `e07b255cd6dd400ee418a8747ad19446723ce430`, build/deploy success.
- Eventos e app logs após deploy: sem novos registros na janela consultada.
- Fonte `intent.py` no commit Live contém filtro `tag1 > 0 AND tag2 > 0`; o SHA do blob é `24d320cc2be6006d628e0d7e6832b924fca5ca63`.
- `/api/status` reporta publicação/ads desativados, catálogo bloqueado sem fonte autorizada, ranking `registered_fail_closed`. Tentativa HTTP de `/api/status` não acessível pelo navegador.

## P0 — Neon
**Produção** (`long-tooth-35390946`, branch `br-spring-hall-b5ed425u`): Ready, PostgreSQL 17, schema público vazio, zero snapshots, schedule vazio.

**Staging** (`floral-hat-53843763`, branch `br-autumn-salad-b4cg34pj`): Ready, 15 tabelas públicas.
- `product_offers`: 19 total/ativas, 0 disponíveis, 0 provider_verified, 0 com preço positivo, 0 com comissão positiva, 0 atualizadas em 7 dias.
- `offers`: 20 total, 19 ativas; `partners`: 2, 1 ativo.
- `clicks`, `conversions`, `outbound_action_tokens`, `affiliate_conversion_audit`, `affiliate_conversion_ledger`, `catalog_visits`, `offer_landing_visits`: 0.
- `ops_persistence_probe`: 61. Último registro readback: `paradigma-auto11-20261128-0011-bst`, 03:13:44 UTC (00:13:44 BRT), propósito operacional de staging; não é evento comercial.
- Snapshots em produção e staging: 0; schedule vazio. Restore isolado não comprovado.
- Quota Neon reset: 01/12/2026 00:00 UTC.

## P0 — GitHub / código
Main Wero1Mercados SHA: `1b17084ee04c910d19a694bf79dd4f6bb4ea4516`.
- `/api/tags/trends`: main não exige clique positivo/recente.
- `/api/premium/ai-ranking`: main não filtra zero cliques nem atividade dos últimos 7 dias.
- Health main usa `SELECT 1` para definir `storage_persistent=true`; isso comprova conectividade, não persistência durável.
- Conversão manual main já rejeita ingestão sem proveniência autenticada (403 via gate).

**Candidatas**
- PR #137, HEAD `d49bb705c8500acf4620482f209acc5a6ece4328`: 4/4 workflows success (P0 Double Check, Wero1 campaign, Commercial Contract e PostgreSQL isolado PG17/18). Filtro de clique positivo e recente no ranking; /go/ sem visita/token para prefetch; /out/ token curto, vinculado e de uso único; health não afirma persistência durável com `SELECT 1`. Draft.
- PR #140, HEAD `05306f2efe9af0d4fb7d147294a5bcce4c574b09`: 4/4 workflows success; fail-closed até adapter autenticado. Draft.
- PR #141, HEAD `3187aea0ac32bfb4ce539c4154ddbc9e70dcbb2e`: 4/4 workflows success; cards passam pelo `/go/` protegido. Draft.
- PR #138: 8 workflows success (runs de dois commits); fingerprint de staging exige identidade HMAC, compare constante, bloqueia DDL/seeds sem identidade correta. Draft.
- PR #139: fingerprint full SHA-256 HMAC; nenhum workflow run retornado para HEAD. Draft, não homologado.
- Wero1Divulgação PR #47: 2/2 success; TAG1 e TAG2 positivas individualmente. Draft.
- PR #50: 2/2 success; status fail-closed explícito. Draft.

Nenhuma PR foi mesclada. CI aprovado é teste de código; não substitui runtime staging, backup/restore e rollback.

## P1 — Metricool
Marca NeyMareSol, ID 7259526:
- Instagram conectado `@neymaresoloficial`, diferente do desejado `@neymaresol`.
- Facebook e TikTok conectados.
- Agendamentos 28/11 07:18–05/12 23:59 BRT: 0.
- TikTok, 21–28/11: 25 vídeos, 677 views, 66 likes, 2 comments, 0 shares (68 interações calculadas como likes+comments; sem shares).
- Followers snapshots: 6.103 em 23/11 e 6.091 em 26/11; mudança diária reportada em 26/11: -12.
- Instagram: 45 seguidores nos snapshots 21–26/11; métricas de posts/reels retornadas como zero ou ausentes no dia 28.
- Facebook: snapshot retornado de 2 seguidores em 21–26/11; linha 28/11 mostra zero para interações/reach/comments/shares/reels. A ferramenta conectada não oferece listagem de posts publicados; não inferir ausência de publicações.
- Melhor horário sábado: Facebook 10h score 8.850; TikTok 10h score 852. Instagram sem score positivo. Scores são recomendações relativas, não previsões de venda.

Nenhuma publicação foi criada ou agendada. Atribuição por campanha continua sem dados.

## Sinal público/editorial
Senacon/MJSP, cartilha de 25/11/2026, orienta pesquisar preço histórico, comparar valor final (frete, taxas e juros), verificar reputação/URL da loja, confirmar destinatário de Pix/boleto, guardar comprovantes e desconfiar de urgência artificial.
Fonte oficial: https://www.gov.br/secom/pt-br/acompanhe-a-secom/noticias/2026/11/cartilha-do-ministerio-da-justica-e-seguranca-publica-orienta-consumidores-nas-compras-da-black-friday

Ideia orgânica (não publicada): vídeo Werozinha — “4 checagens antes do clique: preço histórico, preço total, domínio/vendedor e beneficiário do pagamento”.

## Integridade financeira
Vendas comprovadas: 0 · Conversões confirmadas: 0 · Comissões: R$ 0,00 · Pagamentos: R$ 0,00.

## Gates
1. Recuperar/migrar PostgreSQL produção.
2. Backup e restore isolado.
3. Provar Render staging → Neon staging isolado.
4. Homologar HTTP `/health`, `/ready`, `/go/`, `/out/` sem eventos comerciais sintéticos.
5. Adapter autenticado dos parceiros.
6. Double Check integrado, CI direto #139 e rollback.
7. Só então considerar promoção.

Nesta rodada, apenas documentação foi escrita em branch isolada. Nenhuma mudança em Render/Neon, deploy, merge, publicação, gasto, click, conversão, venda, comissão ou pagamento. Wero1Operário e Wero1Elétrico intocados.

**HOLD mantido.**