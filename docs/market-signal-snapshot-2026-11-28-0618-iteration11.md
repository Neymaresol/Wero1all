# PARADIGMA — Iteração 11 (28/11/2026 06:18 BRT)

## Decisão
**HOLD — produção não liberada.** Inspeção somente leitura de Render, Neon, GitHub e Metricool. Nenhum merge/deploy, publicação, gasto ou evento comercial sintético. Wero1Operário e Wero1Elétrico não foram alterados.

## P0 — Render
- Workspace confirmado: My Workspace.
- Produção Wero1Mercados: serviço `srv-db2fvq4s728c73cahjq0`, `main`, Free, autoDeploy=commit, 1 instância, não suspenso, Health Check Path vazio, Oregon.
- PostgreSQL Render: nenhum instance listado. ID antigo `dpg-db2h93h7lnhs73ev17og-a` não encontrado (404); expiração informada 2026-11-05 já passou.
- Último deploy Live: 2026-10-23, commit `80018a1c3b4a41d8bb052ddf798b11b10d613afa`.
- Eventos: página mais recente retornou 20 `server_failed`, todos exit code 3; há cursor, portanto não é contagem total. Falhas recentes concentradas em 27/11 18:44–18:54 UTC.
- Logs de startup: `psycopg.OperationalError` por DNS não resolver o host PostgreSQL antigo, seguido de `Application startup failed`.
- CPU, memória, instâncias, HTTP request count e latency sem séries. Bandwidth tem pontos pequenos/isolados; não comprova uptime.

## Render staging
- Wero1Mercados staging: `srv-db6k648473hc73dkvk70`, branch `dev/p0-provider-reconciliation-20261012`, autoDeploy desligado, Health Check Path vazio. Eventos/logs/métricas da janela consultada sem registros.
- Wero1Divulgação staging: `srv-db79kdm7bikc73a1rv20`, branch `feat/wero1divulgacao-bootstrap`, autoDeploy desligado, Health Check Path vazio. Último deploy conhecido 25/11 05:24:58 UTC, build/deploy succeeded. Eventos posteriores e logs/métricas consultados sem registros.
- GET /health e /ready não acessíveis pela ferramenta HTTP nesta rodada; status runtime não homologado. Não foram enviados GET mutáveis para /go/ nem POST para /out/.

## Neon
- Produção `long-tooth-35390946`, branch default `br-spring-hall-b5ed425u`, Ready, PostgreSQL 17: 0 tabelas públicas, 0 snapshots, schedule vazio.
- Staging `floral-hat-53843763`, branch default `br-autumn-salad-b4cg34pj`, Ready, PostgreSQL 17: 15 tabelas.
- Read-only SQL staging: product_offers=19, active=19, available=0, provider_verified=0, positive price=0, positive commission=0, updated_7d=0; offers=20, partners=2; clicks/conversions/tokens/audit/ledger/catalog visits/landing visits=0; ops_persistence_probe=61.
- Último probe: `paradigma-auto11-20261128-0011-bst`, 2026-11-28 03:13:44.558 UTC; finalidade operacional staging, não comercial. Readback confirmado; nenhum novo probe escrito.
- Backup/restore isolado não comprovado. Quota Neon reseta em 2026-12-01 00:00 UTC.

## GitHub — main vs candidatas
- Main Wero1Mercados SHA `1b17084ee04c910d19a694bf79dd4f6bb4ea4516`: startup ainda chama `init_db()` e seeds; `/api/tags/trends` não filtra clique positivo/recente; `/go/` GET registra landing; `/out/` POST registra clique sem token.
- PR #137 HEAD `d49bb705c8500acf4620482f209acc5a6ece4328`: **4/4 workflows success** diretamente associados ao HEAD (PARADIGMA P0, Wero1 campaign, Commercial Contract, Isolated PostgreSQL PG17/PG18). Candidata inclui startup opt-in somente staging, health com persistência NOT_VERIFIED, /ready, filtros de clique recente de 7 dias, prefetch guard, token outbound curto/único e INT fail-closed.
- PR #140 HEAD `05306f2efe9af0d4fb7d147294a5bcce4c574b09`: 4/4 workflows success. Adapter autenticado ainda não integrado; flag disponível=false, report manual/hash/caller não desbloqueiam conversão.
- PR #141 HEAD `3187aea0ac32bfb4ce539c4154ddbc9e70dcbb2e`: 4/4 workflows success. Vitrine usa /go/ protegido; não prova runtime HTTP.
- Wero1Divulgação PR #47 HEAD `e4d47ecdf101b3184db8d8660b02bb2de107873c`: 2/2 workflows success; exige TAG1 e TAG2 positivos separadamente, sinais caller_supplied continuam consultivos.
- PR #50 HEAD `b8203686def6e9036a19425f7dec135b0d0cb6f5`: 2/2 workflows success; status explicitamente registered_fail_closed.
- Todas as PRs acima permanecem abertas e Draft. Status combinado do commit não retornou checks; runs de workflow foram consultados e são a evidência dos sucessos. Não foi disparado CI novo.

## Metricool
- Marca NeyMareSol (ID 7259526); Instagram conectado `@neymaresoloficial`, diferente do alvo `@neymaresol`; Facebook e TikTok conectados.
- Agendamentos 28/11–05/12: 0.
- Analytics 21–28/11: TikTok 25 vídeos, 677 views, 66 likes, 2 comments, 0 shares, reach não retornado. Instagram feed posts=0 linhas; Facebook feed posts=0 linhas; SmartLinks timeline=0 linhas.
- Melhores horários relativos: Facebook — sábado 10h (8.850), domingo 10h (7.653), seg 10h (15.247), ter 10h (14.999), qua 12h (15.834), qui 10h (12.351), sex 10h (12.767. TikTok — sáb 10h (852), dom 10h (816), seg 18h (1.096), ter 10h (1.136), qua 10h (1.432), qui 10h (1.471), sex 10h (1.379. Scores relativos, não previsão de vendas.
- Nenhuma publicação, agendamento, SmartLink ou atribuição por campanha criado nesta rodada.

## Sinal editorial autorizado
Senacon/MJSP publicou em 25/11/2026 a cartilha **Black Friday nas compras on-line**, recomendando pesquisar preços anteriores, comparar total com frete/taxas/juros, checar reputação/URL e destinatário Pix/boleto, guardar comprovantes e evitar urgência artificial.
Fonte oficial: https://www.gov.br/mj/pt-br/assuntos/noticias/senacon-lanca-cartilha-com-orientacoes-para-compras-seguras-na-black-friday

## Integridade financeira
Vendas comprovadas=0; conversões=0; comissões=R$ 0,00; pagamentos=R$ 0,00.

## Gates
1. Recuperar/migrar PostgreSQL de produção.
2. Backup e restore isolado comprovados.
3. Comprovar isolamento Render staging → Neon staging.
4. Homologar HTTP /health, /ready, /go/ e /out/ sem eventos comerciais artificiais.
5. Adapter de parceiro autenticado.
6. Double Check combinado e rollback.
7. Só depois considerar promoção.

**Escrita nesta rodada:** este relatório documental na branch isolada da PR #51. Nenhuma alteração em Render/Neon, merge, deploy, anúncio, gasto, publicação ou venda sintética.
