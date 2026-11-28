# PARADIGMA — Iteração 17 (27/11/2026, 13:11 BRT)

## Decisão
**HOLD.** Nenhuma promoção, merge, deploy ou publicação. Nenhuma venda, conversão, comissão ou pagamento sintético. Wero1Operário e Wero1Elétrico fora do escopo.

## P0 — Render / produção Wero1Mercados
- Serviço `srv-db2fvq4s728c73cahjq0`, `main`, Free/Oregon, auto-deploy por commit, não suspenso.
- `healthCheckPath` vazio; métricas de CPU, memória, instâncias, HTTP e latência sem séries na janela 10:00–16:12 UTC.
- Nenhum PostgreSQL na conta. Consulta direta ao ID `dpg-db2h93h7lnhs73ev17og-a` retorna HTTP 404.
- Deploy Live permanece no commit `80018a1c3b4a41d8bb052ddf798b11b10d613afa`, criado em 23/10.
- A primeira página de eventos retorna 10 `server_failed` recentes com exit code 3 (há cursor para eventos adicionais). Logs confirmam falha de DNS ao resolver o host PostgreSQL em 27/11 às 01:09, 01:11 e 01:19 BRT, seguida de `Application startup failed`.
- Não houve eventos nem logs na janela mais recente consultada, 07:00–13:12 BRT. Isso não comprova health; apenas ausência de eventos/logs nessa janela.
- Teste HTTP de `/health` não foi concluído pelo navegador; health runtime permanece não verificado.
- A expiração informada para 05/11/2026 já passou.

## P0 — Render staging
- Wero1Mercados staging `srv-db6k648473hc73dkvk70`: branch antiga `dev/p0-provider-reconciliation-20261012`, auto-deploy desligado, health path vazio; sem métricas/eventos/logs na janela consultada.
- Wero1Divulgação staging `srv-db79kdm7bikc73a1rv20`: branch `feat/wero1divulgacao-bootstrap`, auto-deploy desligado, health path vazio; sem métricas/eventos/logs na janela consultada.
- `wero1divulgacao/app.py` não existe na branch `main` de Wero1all (GitHub 404); a integração principal não está comprovada.

## P0 — Neon
- Produção `long-tooth-35390946`, branch main Ready: 0 tabelas públicas, 0 snapshots e schedule vazio. Quota Free com reset informado em `2026-12-01T00:00:00Z`.
- Staging `floral-hat-53843763`, branch main Ready: 15 tabelas públicas; 0 snapshots e schedule vazio.
- SQL read-only: `product_offers` = 19 total / 19 active / 0 available / 0 provider_verified / 0 com preço positivo / 0 com comissão positiva / 0 atualizadas nos últimos 7 dias.
- Tabela legada `offers` = 20; partners = 2; products = 19; categories = 12.
- clicks = 0; conversions = 0; outbound_action_tokens = 0; conversion_audit = 0; commission_ledger = 0.
- Readback SQL de `ops_persistence_probe` confirmou 59 registros. Registro mais recente `paradigma-auto11-20261127-0917-bst`, checked_at 09:27 BRT; finalidade explicitamente operacional, sem evento comercial. Nenhuma escrita foi feita nesta iteração.
- Restore de backup não comprovado.

## P0 — Código main e candidato
- Main implantada ainda executa `init_db()` e seeds no startup.
- `/health` marca `storage_persistent` igual a `SELECT 1`; isso não prova durabilidade.
- GET `/go/{offer_id}` insere `offer_landing_visits`; o formulário encaminha para POST `/out/{offer_id}`.
- POST `/out/{offer_id}` grava clique sem token de ação de uso único.
- `/api/premium/ai-ranking` ordena ofertas ativas sem `HAVING` ou filtro de cliques positivos/recência; portanto pode incluir ofertas com zero cliques. A rota consultiva `/api/acquisition` tem `HAVING COUNT(c.id) > 0`, mas não exige recência de sete dias.
- Importante: os esquemas `product_offers` e `offers` não possuem colunas INT.1/INT.2. O ranking atual é baseado em cliques, não em INT autenticado. A qualificação INT deve continuar fail-closed.
- PR #137 (Draft, aberta) propõe: clique total > 0, clique nos últimos 7 dias, GET /go sem contabilizar clique, prefetch 204, token de ação curto/uso único em /out, startup side-effect-free por padrão e health sem falsa prova de persistência.
- Quatro workflows do HEAD `d49bb705c8500acf4620482f209acc5a6ece4328` concluídos com sucesso: PARADIGMA P0 Double Check, Wero1 campaign checks, P0 Commercial Contract Double Check e P0 Isolated PostgreSQL PG17/PG18.
- PR #98 também apresenta quatro workflows success, mas permanece Draft. PR #140 continua fail-closed; não existe adapter autenticado de parceiro integrado. PRs não foram mescladas.

## P1 — Metricool
- Brand ID 7259526, NeyMareSol, timezone America/Sao_Paulo.
- Instagram conectado: `@neymaresoloficial`; perfil pretendido: `@neymaresol` — divergência permanece.
- Facebook conectado; TikTok conectado como `neymaresoltiktok`.
- Posts agendados de 27/11 a 04/12: 0.
- Analytics Facebook: sem linhas; Instagram: sem linhas; SmartLinks: sem linhas.
- TikTok: 25 vídeos retornados entre 21/11 e 27/11; 677 visualizações, 66 likes, 2 comentários, 0 compartilhamentos. Em 27/11: 9 vídeos, 161 views, 11 likes, 0 comentários e 0 compartilhamentos.
- Scores relativos do Metricool para sexta-feira: Facebook tem maior score histórico às 10h (12.767); após 13:11, próximo horário útil mais forte é 15h (9.886). TikTok tem maior score histórico às 10h (1.379); próximo horário útil mais forte é 18h (1.222). Scores não são garantia de alcance/vendas. Nenhuma publicação foi criada/agendada.

## P1 — Sinais públicos
- Procon-ES, atualização de 26/11: pesquisa de mais de 40 produtos com variação de até 230%; orienta comparar histórico, preço final, frete e condições de pagamento.
- Procon-MT, 20/11: monitorava 30 produtos em Amazon, Mercado Livre, Magalu, Casas Bahia e Americanas; havia 262 preços online e 438 presenciais coletados, com coleta final prevista para 30/11. Relatou alta semanal de 54% no OMO 3L e 22% em geladeira Brastemp na Amazon entre duas coletas.
- Esses sinais são editoriais/consultivos; não autenticam catálogo, oferta afiliada, INT ou conversão.

## Integridade
- Nenhuma escrita no Neon nesta iteração; nenhuma alteração Render; nenhum merge/deploy; nenhum clique, conversão, venda, comissão, pagamento, anúncio pago ou publicação sintética.
- Wero1Operário e Wero1Elétrico permaneceram intocados.

## Gates seguintes
1. Recuperar/migrar PostgreSQL de produção e verificar o destino de dados.
2. Provar backup restaurável e restore isolado.
3. Comprovar que Render staging aponta exclusivamente para Neon staging.
4. Provisionar segredo HMAC por canal seguro.
5. Homologar /health, /ready, /go e /out em staging isolado.
6. Integrar adapter de parceiro com autenticação, identidade, assinatura, unicidade e replay protection.
7. Consolidar PRs empilhadas, executar Double Check integrado e comprovar rollback antes de qualquer promoção.
