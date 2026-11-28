# PARADIGMA — Iteração 18 (27/11/2026, 14:15 BRT)

## Decisão
**HOLD.** Nenhuma promoção comercial, merge ou deploy de produção. Esta atualização é documental, em branch isolada da PR #51.

## P0 — Render / Wero1Mercados produção
- Workspace: My Workspace.
- Serviço `wero1mercados`, ID `srv-db2fvq4s728c73cahjq0`, branch `main`, plano Free, auto-deploy por commit ativo, `healthCheckPath` vazio, serviço não suspenso.
- `list_postgres_instances`: nenhum PostgreSQL na conta.
- Consulta direta a `dpg-db2h93h7lnhs73ev17og-a`: 404.
- Eventos Render retornados: 25 eventos na primeira página, todos `server_failed` com `nonZeroExit=3`; mais recente em 27/11 04:19:14Z (01:19 BRT).
- Deploy Live ainda usa `80018a1c3b4a41d8bb052ddf798b11b10d613afa`, criado em 23/10.
- Logs de 27/11 13:00Z–17:20Z: 0 registros. Métricas CPU, memória, instâncias, HTTP e latência: arrays vazios.
- GET `/health` não pôde ser verificado pelo navegador disponível. Não declarar health saudável.
- A expiração informada de 05/11/2026 já passou.

## P0 — Neon: produção versus staging
### Produção
- Projeto `long-tooth-35390946`, branch default `br-spring-hall-b5ed425u`, Ready.
- SQL read-only: 0 tabelas públicas.
- Snapshots: 0; schedule automático: vazio.

### Staging
- Projeto `floral-hat-53843763`, branch default `br-autumn-salad-b4cg34pj`, Ready.
- SQL read-only: 15 tabelas públicas.
- `product_offers`: 19 totais, 19 ativas, 0 disponíveis, 0 `provider_verified`, 0 com preço positivo, 0 com comissão positiva, 0 atualizadas em 7 dias; elegíveis = 0.
- `offers` legado = 20; `partners` = 2; `products` = 19.
- Cliques = 0; conversões = 0; tokens outbound = 0; auditoria de conversões = 0; ledger de comissões = 0.
- `ops_persistence_probe`: 59 registros; último `checked_at` = 2026-11-27 12:27:24.570Z (09:27 BRT). Esse registro é anterior a esta iteração; não houve nova escrita.
- Snapshots = 0; schedule automático vazio.

### Contrato de esquema observado em staging
- `product_offers.provider_verified` é boolean com default false; não há colunas INT.1/INT.2.
- `conversions` contém external_id, offer_id, status, sale_amount_brl, commission_brl e confirmed_at; o esquema não demonstra autenticação da origem do parceiro.
- `affiliate_conversion_audit` guarda source_partner, source_account, external_id, source_report e source_sha256, mas hash do relatório por si só não autentica o emissor.
- `outbound_action_tokens` guarda token_hash, offer_id, channel, campaign, created_at e consumed_at; não há coluna expires_at. A expiração precisa ser aplicada e testada no token assinado.
- Persistência de staging foi consultada via SQL read-only; backup restaurável e vínculo Render staging → Neon staging continuam não comprovados.

## P0 — GitHub / segurança
- Main de Wero1Mercados permanece em `80018a1c3b4a41d8bb052ddf798b11b10d613afa`.
- PR #137 aberta, Draft, 48 commits, 20 arquivos; HEAD `d49bb705c8500acf4620482f209acc5a6ece4328`, base main. Quatro workflows concluídos com sucesso: PARADIGMA P0 Double Check, Wero1 campaign checks, P0 Commercial Contract Double Check e P0 Isolated PostgreSQL Double Check (PG17/PG18).
- PR #140 aberta, Draft, empilhada sobre #137; HEAD `05306f2efe9af0d4fb7d147294a5bcce4c574b09`. Quatro workflows concluídos com sucesso. O próprio escopo mantém `AUTHENTICATED_ADAPTER_AVAILABLE = False`; conversões seguem bloqueadas até adapter server-side autenticado.
- PR #141 aberta, Draft, empilhada sobre #137; HEAD `3187aea0ac32bfb4ce539c4154ddbc9e70dcbb2e`. Quatro workflows concluídos com sucesso; vitrine candidata aponta para `/go/{offer_id}`, sem validar runtime.
- Status checks combinados retornaram lista vazia; evidência de CI vem dos workflow runs acima.
- PRs não foram mescladas. Não executar GET `/go/` na main: a versão Live ainda pode gravar visita. POST `/out/` não foi testado sem token e staging isolado. Nenhuma conversão sintética.

## P1 — Wero1Divulgação / Render staging
- Serviço `wero1divulgacao-staging`, ID `srv-db79kdm7bikc73a1rv20`, branch `feat/wero1divulgacao-bootstrap`, Free, auto-deploy desligado, health check vazio.
- Deploy Live de 25/11 05:24Z, commit `e07b255cd6dd400ee418a8747ad19446723ce430`, build e deploy succeeded.
- Logs 27/11 13:00Z–17:20Z: 0 registros; health HTTP não comprovado.
- Código da branch: `0.4.0-dev`; `/health` declara modo staging e publicação false; `/api/status` declara integrações não configuradas, catálogo bloqueado sem fonte autorizada, ranking bloqueado sem sinais autorizados e campanhas publicadas = 0.
- `intent.py` exige TAG1 > 0 E TAG2 > 0 para ranking consultivo. Esses sinais caller-supplied não autenticam INT.1/INT.2.
- Serviço `wero1mercados-staging`, ID `srv-db6k648473hc73dkvk70`, continua na branch antiga `dev/p0-provider-reconciliation-20261012`, auto-deploy desligado, health check vazio, sem eventos/logs na janela. Conexão ao Neon staging não comprovada.

## P1 — Metricool
- Brand NeyMareSol, ID 7259526, timezone America/Sao_Paulo.
- Instagram conectado: `@neymaresoloficial`; desejado: `@neymaresol` — divergência confirmada.
- Facebook conectado (ID 102552892426549); TikTok conectado (`neymaresoltiktok`).
- Posts agendados de 27/11 14:15 a 04/12 23:59 BRT: 0.
- Analytics 20–27/11: Facebook retornou 2 seguidores nos snapshots de 20–26/11 e, em 27/11, 0 feed posts, 0 interações e 0 impressões; Instagram retornou 45 seguidores em 20–26/11 e, em 27/11, 0 feed posts/views/reach/interações.
- TikTok: 25 vídeos, 677 visualizações, 66 likes, 2 comentários e 0 compartilhamentos no período.
- SmartLinks timeline: nenhuma linha; atribuição por campanha não comprovada.
- Melhor janela próxima sugerida pelo Metricool: sábado 28/11, Facebook 10h (score 8.850) e TikTok 10h (score 852); Instagram scores 0 em todos os horários. Scores são relativos, não previsão de resultado. Nenhuma publicação criada ou agendada.

## P1 — Sinal público autorizado (editorial)
- Procon Mogi das Cruzes, notícia publicada nesta semana para a Black Friday de 27/11: comparar preço entre lojas e valor final com frete, condições de pagamento, prazo de entrega e troca.
- Procon Aracaju, 26/11: pesquisa de preços coletada em 25/11; valores variam por produto/modelo/loja e podem mudar. Recomenda conferir reputação, segurança do site e guardar anúncio/comprovante.
- Uso permitido nesta etapa: pauta educativa e checklist editorial. Não são feed de afiliados, catálogo autorizado, prova de oferta, intenção INT, clique ou venda.
- Fontes: https://www.mogidascruzes.sp.gov.br/noticia/procon-de-mogi-orienta-consumidor-a-comparar-precos-antes-de-comprar-na-black-friday ; https://procon.aracaju.se.gov.br/black-friday-procon-aracaju-orienta-consumidores-a-comparar-precos-e-evitar-falsas-promocoes/

## Segurança e limites desta iteração
- Nenhuma escrita em Render, Neon ou Metricool.
- Nenhum merge, deploy, anúncio, gasto, publicação, clique sintético, conversão, venda, comissão ou pagamento.
- Wero1Operário e Wero1Elétrico intocados.
- Produção permanece HOLD até recuperar/migrar PostgreSQL, comprovar backup/restore, provar isolamento staging, provisionar HMAC por canal seguro, homologar health e rotas em staging, integrar adapter autenticado, Double Check integrado e rollback.
