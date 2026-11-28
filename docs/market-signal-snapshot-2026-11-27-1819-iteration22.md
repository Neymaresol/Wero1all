# PARADIGMA — Iteração 22
Data: 27/11/2026, 18:19 BRT
Escopo: Wero1Mercados / Wero1Divulgação
Decisão: HOLD — sem promoção comercial ou deploy de produção.

## 1. Render — produção Wero1Mercados

Workspace: My Workspace (`tea-dao62kn40ujc73e210eg`).
Serviço: `wero1mercados` (`srv-db2fvq4s728c73cahjq0`), branch `main`, Oregon, plano Free, auto-deploy por commit ativo, serviço não suspenso, Health Check Path vazio.
Render lista zero instâncias PostgreSQL. A consulta direta a `dpg-db2h93h7lnhs73ev17og-a` retornou HTTP 404.

Eventos consultados em 27/11 entre 17:00 e 21:15 UTC: cinco `server_failed`, todos exit code 3, entre 18:44 e 18:54 UTC (15:44–15:54 BRT). Segunda página de eventos vazia. Logs filtrados confirmaram repetidamente:
`psycopg.OperationalError: failed to resolve host 'dpg-db2h93h7lnhs73ev17og-a'`
seguido de `Application startup failed. Exiting.`
Não há séries de CPU, memória, instâncias, HTTP ou latência no período consultado. GET público de `/health` não ficou acessível pela ferramenta; health runtime não comprovado.

A expiração informada de 05/11/2026 já passou. Não houve alteração de configuração, reinício ou deploy.

## 2. Render — staging

Wero1Mercados staging: `srv-db6k648473hc73dkvk70`, branch antiga `dev/p0-provider-reconciliation-20261012`, auto-deploy desligado, Health Check Path vazio.
Wero1Divulgação staging: `srv-db79kdm7bikc73a1rv20`, branch `feat/wero1divulgacao-bootstrap`, auto-deploy desligado, Health Check Path vazio.
Os endpoints públicos `/health` e `/ready` de Wero1Mercados staging não ficaram acessíveis pela ferramenta. Não foi comprovada conexão Render staging → Neon staging. Nenhum deploy foi executado.

## 3. Neon — produção e staging

Produção: projeto `long-tooth-35390946`, branch `br-spring-hall-b5ed425u`, Ready, PostgreSQL 17; zero tabelas públicas, zero snapshots e schedule vazio.
Staging: projeto `floral-hat-53843763`, branch `br-autumn-salad-b4cg34pj`, Ready, PostgreSQL 17; 15 tabelas públicas, zero snapshots e schedule vazio.
Quota reset informada pelos metadados do projeto: 01/12/2026 00:00 UTC. Isso é reset de quota Neon, distinto da expiração já passada do PostgreSQL antigo do Render.

### SQL read-only de staging

- product_offers: 19; ativas: 19.
- Disponíveis: 0; provider_verified: 0.
- Preço positivo: 0; comissão positiva: 0; atualizadas em 7 dias: 0.
- Ofertas legadas: 20, das quais 19 ativas.
- Parceiros: 2; produtos: 19.
- Cliques: 0; conversões: 0; outbound tokens: 0.
- Auditorias de conversão: 0; ledger de comissões: 0.
- offer_landing_visits: 0; catalog_visits: 0.
- Probes operacionais antes do teste: 59.

A consulta a `information_schema.columns` não encontrou nenhuma coluna pública com nome contendo “int”; INT.1/INT.2 não existem no esquema atual.

### Teste de persistência staging

Verificado que o probe `paradigma-auto11-20261127-1814-bst` não existia. Inserido somente em Neon staging na tabela `ops_persistence_probe`, com finalidade explícita de persistência operacional e sem evento comercial. INSERT ... RETURNING e SELECT independente recuperaram o mesmo `probe_id`, timestamp `2026-11-27T21:19:21.712Z` e propósito. Resultado: write/readback de staging confirmado. Nenhuma escrita em produção.

### Esquema relevante

`product_offers` contém `provider_verified`, mas não INT.1/INT.2.
`outbound_action_tokens` contém `token_hash`, `offer_id`, `channel`, `campaign`, `created_at`, `consumed_at`; não contém `expires_at`. A candidata #137 aplica TTL de dez minutos usando `created_at`.
`conversions` contém `external_id` único, oferta, status, valores e confirmação. Hash SHA-256 isolado não autentica identidade do parceiro.

## 4. GitHub — Wero1Mercados

Main continua com os defeitos:
- startup executa DDL/seeds;
- `/health` usa `SELECT 1` e marca `storage_persistent=true` a partir de conectividade;
- `/api/tags/trends` inclui ofertas sem clique, pois usa LEFT JOIN sem HAVING;
- GET `/go/{offer_id}` grava visita e não possui token de ação;
- POST `/out/{offer_id}` legado não exige token de uso único.

Candidatas isoladas:
- PR #137, Draft/open, HEAD `d49bb705c8500acf4620482f209acc5a6ece4328`, 48 commits/20 arquivos. CI: quatro workflows success (PARADIGMA P0, Wero1 campaign, Commercial Contract, PostgreSQL 17/18). Corrige ranking com clique positivo e recente (7 dias), prefetch, token curto/único em /out/, startup fail-closed e health que não confunde conectividade com persistência.
- PR #140, Draft/open, HEAD `05306f2efe9af0d4fb7d147294a5bcce4c574b09`. CI: quatro workflows success. `AUTHENTICATED_ADAPTER_AVAILABLE=False`; conversões permanecem bloqueadas mesmo com booleano verified e hash correspondente.
- PR #141, Draft/open, HEAD `3187aea0ac32bfb4ce539c4154ddbc9e70dcbb2e`. CI: quatro workflows success. Cartões da vitrine apontam para /go/.

Nenhuma PR foi mesclada. CI em PostgreSQL descartável não equivale a homologação HTTP no Render. Não foram executadas rotas /go/ ou /out/ em produção nem em staging.

## 5. Wero1Divulgação

Render staging permanece na branch `feat/wero1divulgacao-bootstrap`, auto-deploy desligado e Health Check Path vazio.
Código GitHub consultado: `0.4.0-dev`. A rota /health do código retorna status estático “ok”; não é prova de runtime. /api/status mantém publicação e anúncios pagos desativados, integrações não configuradas, catálogo bloqueado por ausência de fonte autorizada e ranking INT bloqueado por ausência de fonte autorizada.
`intent.py` exige TAG1 > 0 e TAG2 > 0 independentemente, mas os sinais são caller-supplied e apenas consultivos.
- PR #47, Draft/open, HEAD `e4d47ecdf101b3184db8d8660b02bb2de107873c`: dois workflows Double Check success.
- PR #50, Draft/open, HEAD `b8203686def6e9036a19425f7dec135b0d0cb6f5`: dois workflows Double Check success.
Nenhuma publicação ou simulação comercial foi executada.

## 6. Metricool — marca NeyMareSol

Brand ID 7259526; timezone America/Sao_Paulo.
- Instagram conectado: `@neymaresoloficial`; desejado: `@neymaresol` — divergência confirmada.
- Facebook conectado (ID de página 102552892426549).
- TikTok conectado (`neymaresoltiktok`).

Período analítico 20–27/11:
- Facebook: 2 seguidores nos snapshots 20–26/11; conteúdo e interações retornados como zero em 27/11.
- Instagram: 45 seguidores nos snapshots 20–26/11; conteúdo, views e interações retornados como zero em 27/11.
- TikTok: 25 vídeos (14 em 21/11, 2 em 25/11, 9 em 27/11), 677 views, 66 likes, 2 comentários, 0 compartilhamentos. Snapshots de seguidores: 6.103 em 23/11 e 6.091 em 26/11.
- SmartLinks: nenhuma linha de timeline.
- Agendamentos 27/11 18:14–04/12 23:59 BRT: zero.

Sugestões do Metricool para sábado, 28/11: Facebook 10h (score 8.850) e TikTok 10h (score 852). Instagram: todos os scores consultados iguais a zero. Scores relativos, não previsão de vendas. Nenhum post foi criado ou agendado. Atribuição por campanha não comprovada.

## 7. Sinais públicos/autorizados para pauta

- Procon Sergipe, publicado em 26/11: monitoramento de 20 produtos ao longo de quatro semanas; no online, variação de até 39,15% em ar-condicionado de 12 mil BTUs; em lojas físicas, até 111,23% para sanduicheira e 74,27% para smart TV de 43". O Procon informou que a fiscalização continuaria em 27/11. Fonte: https://sejuc.se.gov.br/procon-sergipe-divulga-pesquisa-de-precos-para-a-black-friday-2026/
- Senacon/MJSP, 25/11: comparar preço total com frete, taxas e juros; verificar reputação/domínio do vendedor; evitar falsa urgência; conferir destinatário de Pix/boleto; guardar comprovantes. Fonte: https://www.gov.br/mj/pt-br/assuntos/noticias/senacon-lanca-cartilha-com-orientacoes-para-compras-seguras-na-black-friday

Uso editorial apenas. Não são ofertas afiliadas, preços atuais do catálogo ou sinais INT autenticados.

## 8. Integridade e decisão

- Uma única escrita operacional: probe não comercial em Neon staging, com readback confirmado.
- Uma escrita documental nesta branch isolada do GitHub.
- Nenhuma escrita em Neon produção ou Render.
- Nenhum merge, deploy, anúncio pago, gasto, publicação, clique, venda, comissão ou pagamento sintético.
- Wero1Operário e Wero1Elétrico não foram alterados.

Financeiro comprovado nesta execução: zero vendas, comissões, conversões ou pagamentos.
Status: HOLD.

Gates antes de qualquer promoção: recuperar/migrar PostgreSQL de produção; backup restaurável e restore isolado; provar isolamento Render staging → Neon staging; integrar adapter de parceiro com autenticação de origem, conta, assinatura/credencial, unicidade e replay; homologar /health, /ready, /go/ e /out/ em staging; Double Check integrado; rollback comprovado.
