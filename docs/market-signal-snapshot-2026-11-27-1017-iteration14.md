# PARADIGMA — Snapshot operacional da Iteração 14
**Data de verificação:** 27/11/2026, 10:17 BRT  
**Escopo:** Wero1Mercados / Wero1Divulgação. Auditoria de Render, Neon, GitHub e Metricool; somente documentação foi gravada nesta rodada.

## Decisão
**HOLD — produção comercial não liberada.** O PostgreSQL Render original continua ausente, o projeto Neon chamado produção existe mas não tem tabelas públicas, staging não tem ofertas elegíveis nem eventos comerciais, e o runtime de staging não foi homologado.

## P0 — Render produção
- Serviço: `wero1mercados`, ID `srv-db2fvq4s728c73cahjq0`, workspace My Workspace.
- Branch `main`, plano Free, auto-deploy por commit ativo, serviço não suspenso.
- Health Check Path vazio; portanto o estado `not_suspended` não comprova health HTTP.
- Nenhuma instância PostgreSQL encontrada na conta Render.
- Consulta direta ao PostgreSQL `dpg-db2h93h7lnhs73ev17og-a`: 404.
- A expiração informada em 05/11/2026 já passou.
- Eventos de 26/11 13:17Z a 27/11 13:17Z: 10 `server_failed`, todos `nonZeroExit=3`; segunda página vazia. Último evento em 27/11 04:19Z (01:19 BRT). Nenhum `server_available` no conjunto consultado.
- Métricas de CPU, memória, instâncias, HTTP requests e latência: séries vazias nas últimas 24h.
- Consulta de logs de aplicação retornou 503 temporário do serviço de logs; não foi possível confirmar logs atuais.
- Último deploy Live: 23/10/2026, commit `80018a1c3b4a41d8bb052ddf798b11b10d613afa`.
- Comparação GitHub `main` versus esse commit: `identical`, 0 commits à frente e 0 atrás. A versão implantada corresponde ao HEAD de produção.
- Nota de integridade: o SHA `1b17084...` retornado por `fetch_file(main.py)` é SHA do blob do arquivo, não SHA do commit. A comparação de commits confirmou o SHA correto do deploy acima.

## P0 — Neon produção e staging
### Projeto Neon produção
- Projeto `wero1mercados-production`, ID `long-tooth-35390946`.
- Branch `main`, ID `br-spring-hall-b5ed425u`, estado Ready.
- Consulta `information_schema.tables`: 0 tabelas públicas.
- Snapshots: 0; schedule automático: vazio.
- Quota gratuita da organização: `quota_reset_at=2026-12-01T00:00:00Z`. Isso é renovação/reset de quota, não prova de expiração do projeto e não substitui o PostgreSQL Render ausente.
- Não há evidência de que Render esteja conectado a esse projeto Neon.

### Projeto Neon staging
- Projeto `wero1mercados-staging`, ID `floral-hat-53843763`.
- Branch `main`, ID `br-autumn-salad-b4cg34pj`, estado Ready.
- 15 tabelas públicas.
- Contagens SQL exatas: `product_offers=19`, ativas=19, disponíveis=0, `provider_verified=0`, `offers=20`, `partners=2`, `clicks=0`, `conversions=0`, `outbound_action_tokens=0`, `affiliate_conversion_audit=0`, `affiliate_conversion_ledger=0`.
- `ops_persistence_probe=59`; último `checked_at=2026-11-27T12:27:24.570Z` (09:27 BRT).
- Snapshots: 0; schedule automático: vazio.
- Nenhum INSERT/UPDATE foi executado no Neon nesta iteração. A presença dos 59 probes é readback de dados anteriores, não uma nova prova de persistência nesta rodada.
- O catálogo staging não tem oferta disponível ou verificada pelo provedor; elegíveis=0. Cliques, conversões e ledger permanecem zerados.

## P0 — código main versus candidatos
### Main atualmente implantada
Leitura do `main.py` no commit implantado:
- Startup chama `init_db()` e seeds sem opt-in explícito.
- `/health` usa `SELECT 1` e retorna `storage_persistent=database_ok`; conectividade é apresentada incorretamente como persistência.
- GET `/go/{offer_id}` grava `offer_landing_visits`.
- POST `/out/{offer_id}` grava clique sem token de ação de uso único.
- `/api/premium/ai-ranking` não tem `HAVING`; inclui ofertas ativas com zero cliques e sem atividade recente.
- Endpoint manual de conversão chama `reject_unverified_manual_conversion` e falha fechado; bearer administrativo não autentica origem de parceiro.
- A main não demonstra pipeline autenticado INT.1/INT.2.

### PR #98 — candidato isolado
- PR aberta/Draft, branch `fix/p0-intent-failclosed-20261023`, HEAD registrado no corpo da PR: `8e1f13a0b8f515869d214ebb6947eee5eb88cf44`, 26 commits à frente e 0 atrás da main.
- Startup exige opt-in explícito para DDL/seeds.
- Health deixa `storage_persistent=null`, `persistence_verified=false` e status `not_verified`; não confunde `SELECT 1` com durabilidade.
- GET `/go/` não grava visita/clique; o POST `/out/` valida e consome token de uso único antes de registrar clique.
- Ranking exige clique total positivo e clique nos últimos sete dias; INT.1/INT.2 continua fail-closed sem evidência autenticada.
- Quatro workflows associados ao HEAD foram consultados nesta rodada e terminaram `completed/success`: Wero1 campaign checks, PARADIGMA P0 Double Check, P0 Commercial Contract Double Check e P0 Isolated PostgreSQL Double Check.
- PR #98 não foi mesclada nem implantada; runtime, identidade do banco, backup/restauração e rollback continuam pendentes.

### PR #137 / #138 / #139 / #140 / #141 — cadeia ainda precisa reconciliação
- PR #137 descreve uma cadeia consolidada com ranking sem zero/cliques antigos, prefetch 204, token de uso único, startup fail-closed e health sem alegação de persistência. O corpo registra quatro workflows de Double Check aprovados; o HEAD de #137 não foi revalidado diretamente nesta rodada.
- PR #138 adiciona fingerprint de identidade do banco staging.
- PR #139 fortalece o fingerprint para HMAC-SHA256 completo.
- PR #140 e #141 são follow-ups empilhadas sobre #137, não sobre #139. Portanto, a proteção de identidade #138/#139 ainda precisa ser incorporada à mesma cadeia antes de homologação.
- Código da branch #140 foi inspecionado: startup exige `WERO_DEPLOYMENT_ENV=staging` e `WERO_ALLOW_STARTUP_DB_MUTATIONS` explícito; o arquivo `main.py` dessa branch não contém `WERO_STAGING_DATABASE_FINGERPRINT` nem guard de identidade.
- Na branch #140, GET `/go/` retorna 204 para prefetch/prerender declarado; navegação normal grava visita e token de ação; POST `/out/` consome token vinculado à oferta em até 10 minutos e grava clique na mesma transação.
- Ranking candidato #140 exclui zero cliques e cliques sem atividade nos últimos sete dias; separa ranking consultivo de INT.1/INT.2, que continua vazio sem adapter autenticado.
- `p0_conversion_gate.py` define `AUTHENTICATED_ADAPTER_AVAILABLE=False`; relatório com flag `verified=True` ou hash válido continua rejeitado sem adapter server-side.
- CI de PR #140 não foi revalidado diretamente nesta rodada. Não afirmar 4/4 para todos os follow-ups sem consultar cada HEAD.

## P0 — Render staging
- Wero1Mercados staging: serviço `srv-db6k648473hc73dkvk70`, branch `dev/p0-provider-reconciliation-20261012`, auto-deploy desligado, Health Check vazio, último Live em 13/10 no commit `9a3741d30f18d172b2cacc147427b686100694a4`.
- Wero1Divulgação staging: serviço `srv-db79kdm7bikc73a1rv20`, branch `feat/wero1divulgacao-bootstrap`, auto-deploy desligado, Health Check vazio, último Live em 25/11 no commit `e07b255cd6dd400ee418a8747ad19446723ce430`.
- Ambos sem séries de CPU/memória/instâncias/HTTP/latência. Wero1Mercados staging sem eventos no período consultado; Wero1Divulgação staging sem eventos e sem logs de aplicação no período.
- Não foram executados GETs comerciais `/go/` ou POSTs `/out/`. O staging Wero1Mercados está em branch antiga e sua identidade de banco não foi comprovada; por isso não foi acordado para testes que possam acionar startup ou efeitos de banco.
- GET `/api/status` de Wero1Divulgação não pôde ser consultado pelo navegador disponível; runtime não confirmado.

## P1 — Wero1Divulgação
- Código da branch `feat/wero1divulgacao-bootstrap`: publicação desativada, anúncios pagos desativados, integrações não configuradas, planejamento de catálogo bloqueado por falta de fonte autorizada e ranking INT bloqueado por falta de fonte autenticada.
- `intent.py` exige TAG1>0 e TAG2>0 individualmente. Esses sinais são caller-supplied/consultivos e não autenticam INT.1/INT.2.
- PR #47 (TAG1/TAG2) e PR #50 (status fail-closed) continuam abertas; não houve integração de feed/API autorizado nesta rodada.
- Campanhas publicadas: 0.

## P1 — Metricool
- Marca NeyMareSol, ID `7259526`, timezone `America/Sao_Paulo`.
- Instagram conectado: `@neymaresoloficial`; perfil desejado `@neymaresol` continua divergente e não conectado.
- Facebook conectado, página ID `102552892426549`; TikTok conectado `neymaresoltiktok`.
- Posts agendados entre 27/11 e 04/12: 0.
- Facebook feed posts e Instagram feed posts entre 20/11 e 27/11: sem linhas retornadas.
- Métricas agregadas Facebook em 27/11: posts, interações, impressões, total de conteúdo e interações totais = 0.
- Métricas de conta Instagram no período: sem linhas.
- SmartLinks timeline e botões: sem linhas; atribuição por campanha não comprovada.
- TikTok: 14 vídeos retornados, todos em 21/11; 350 views, 43 likes, 2 comentários e 0 compartilhamentos no período consultado.
- Nenhuma publicação foi criada, editada, enviada para revisão ou agendada.

## Integridade
Nenhum merge, deploy, alteração de produção, escrita Neon, publicação Metricool, anúncio pago, gasto, clique, conversão, venda, comissão ou pagamento foi criado nesta iteração. A única escrita foi este documento na branch isolada de documentação. Wero1Operário e Wero1Elétrico permaneceram intocados.

## Gates restantes
1. Recuperar/migrar PostgreSQL de produção com plano aprovado, identidade confirmada, backup restaurável e rollback.
2. Provar que Render staging usa exclusivamente Neon staging; incorporar fingerprint HMAC-SHA256 ao stack final.
3. Homologar `/health`, `/ready`, `/go/` e `/out/` no staging isolado, incluindo prefetch, token expirado, replay e vínculo de oferta.
4. Integrar adapter server-side de parceiro que autentique origem/conta/assinatura, identidade da oferta, deduplicação e replay; manter conversões bloqueadas até lá.
5. Reconciliar PRs empilhadas em uma única cadeia; revalidar CI de cada HEAD, Double Check integrado e rollback.
6. Somente depois reavaliar catálogo, campanha orgânica, SmartLinks/atribuição e promoção.
