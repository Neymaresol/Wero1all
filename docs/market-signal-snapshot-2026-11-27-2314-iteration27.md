# PARADIGMA — Iteração 27 (2026-11-27 23:14 BRT)

**Escopo:** inspeção read-only de GitHub, Neon staging/produção e Metricool. Render ficou bloqueado por ausência de workspace selecionado nesta execução automatizada; nenhum workspace foi escolhido implicitamente.

## 1. Render — bloqueio de inspeção

- A consulta de workspace selecionado retornou `no workspace selected`.
- A ferramenta de inventário de workspaces não foi chamada em execução automatizada; a seleção exige confirmação explícita do usuário.
- Portanto, serviço, banco PostgreSQL, eventos, logs, métricas e health HTTP do Render **não foram revalidados nesta iteração**.
- A expiração informada de `2026-11-05` já passou, mas a existência/ausência atual do recurso Render não foi confirmada nesta rodada.
- Nenhuma alteração de serviço, variável, deploy ou banco foi executada.

## 2. GitHub — produção e candidatas

Repositórios encontrados: `Neymaresol/wero1mercados` e `Neymaresol/Wero1all`, ambos com permissão administrativa disponível à conexão.

Leitura de `main.py` na branch `main` de Wero1Mercados confirmou:
- `startup()` chama `init_db()` e seeds automaticamente.
- `/health` define `storage_persistent` a partir de `SELECT 1`, que só comprova conectividade.
- `/go/{offer_id}` registra visita sem guard de prefetch.
- `/out/{offer_id}` grava clique sem token de ação de uso único.
- `/api/tags/trends` usa LEFT JOIN sem filtro positivo/recente.
- `/api/premium/ai-ranking` usa LEFT JOIN sem HAVING, permitindo ofertas com zero cliques.
- O endpoint legado Amazon one-click grava clique diretamente.

PRs P0 continuam abertas, Draft e sem merge:
- Wero1Mercados #137 — HEAD `d49bb705c8500acf4620482f209acc5a6ece4328`; 4 workflows concluídos com success.
- Wero1Mercados #140 — HEAD `05306f2efe9af0d4fb7d147294a5bcce4c574b09`; 4 workflows success. Baseia-se na branch da #137.
- Wero1Mercados #141 — HEAD `3187aea0ac32bfb4ce539c4154ddbc9e70dcbb2e`; 4 workflows success. Baseia-se na branch da #137.
- Wero1Divulgação #47 — HEAD `e4d47ecdf101b3184db8d8660b02bb2de107873c`; 2 workflows success.
- Wero1Divulgação #50 — HEAD `b8203686def6e9036a19425f7dec135b0d0cb6f5`; 2 workflows success.
- Documentação #51 — HEAD anterior `4374b6a49575db548a613ea2a3bdd548b90d9e8b`; 1 workflow success.

Na candidata #137, o código lido aplica HAVING para clique positivo e clique nos últimos sete dias em `/api/tags/trends` e `/api/premium/ai-ranking`; o funil usa guard de prefetch e token curto, vinculado à oferta e de uso único. CI positivo não substitui homologação HTTP no Render staging.

A candidata #140 mantém `AUTHENTICATED_ADAPTER_AVAILABLE = False`; a ingestão de conversão permanece bloqueada sem adapter server-side autenticado. Booleano informado pelo chamador e SHA-256 isolado não comprovam identidade do parceiro.

## 3. Neon — produção

Projeto `wero1mercados-production`, ID `long-tooth-35390946`, PostgreSQL 17, AWS us-east-2.
- Branch principal `br-spring-hall-b5ed425u`, estado Ready.
- Tabelas no schema público: 0.
- Snapshots: 0.
- Agendamento de snapshots: vazio.
- Quota reset informada: `2026-12-01T00:00:00Z`.

## 4. Neon — staging

Projeto `wero1mercados-staging`, ID `floral-hat-53843763`, PostgreSQL 17, AWS us-east-2.
- Branch principal `br-autumn-salad-b4cg34pj`, estado Ready.
- Tabelas públicas: 15.
- Snapshots: 0.
- Agendamento de snapshots: vazio.

Contagens SQL read-only:
- `product_offers`: 19 total, 19 ativas, 0 disponíveis, 0 `provider_verified`, 0 com preço positivo, 0 com comissão positiva, 0 atualizadas nos últimos 7 dias.
- `offers`: 20.
- `clicks`, `conversions`, `outbound_action_tokens`, `affiliate_conversion_audit`, `affiliate_conversion_ledger`, `catalog_visits`: todos 0.
- `ops_persistence_probe`: 60.

Últimos probes recuperados:
- `paradigma-auto11-20261127-1814-bst`, 2026-11-27T21:19:21.712Z.
- `paradigma-auto11-20261127-0917-bst`, 2026-11-27T12:27:24.570Z.
- `paradigma-iter11-20261127-0018-bst`, 2026-11-27T03:20:52.437Z.

Os probes são exclusivamente operacionais; não são cliques, vendas, conversões, comissões ou pagamentos. Nenhuma escrita SQL foi realizada nesta iteração.

Schema verificado:
- `product_offers` tem `provider_verified`, mas não campos INT.1/INT.2 ou assinatura do emissor.
- `outbound_action_tokens` contém `token_hash`, `offer_id`, `channel`, `campaign`, `created_at`, `consumed_at`; não contém `expires_at`. A candidata aplica TTL pela idade de `created_at`.
- `conversions` contém `external_id`, `offer_id`, status e valores; não autentica a origem por si só.
- `affiliate_conversion_ledger` armazena parceiro, conta, relatório, SHA-256, status e valores. Hash não equivale a assinatura/autenticação da origem.

## 5. Metricool — marca NeyMareSol

Marca ID `7259526`, fuso `America/Sao_Paulo`.
- Instagram conectado: `@neymaresoloficial`; alvo solicitado: `@neymaresol` (divergentes).
- Facebook conectado: ID `102552892426549`.
- TikTok conectado: `neymaresoltiktok`.

Período consultado: 20–28/11/2026.
- Posts agendados entre 27/11 e 05/12: nenhum.
- Analytics de posts Facebook: sem linhas.
- Analytics de posts Instagram: sem linhas.
- SmartLinks timeline: sem linhas.
- TikTok: 25 vídeos, 677 visualizações, 66 likes, 2 comentários, 0 compartilhamentos.
- Último total de seguidores TikTok retornado: 6.091 em 26/11, com variação diária de -12 nesse registro.

Scores relativos de melhor horário para sábado, 28/11:
- Facebook: 10h, 8.850.
- TikTok: 10h, 852.
- Instagram: todos os horários retornaram 0.
Scores não são previsão de vendas. Nenhuma publicação foi criada/agendada; atribuição por campanha não comprovada.

## 6. Sinais públicos autorizados — uso editorial

- Procon-MT, 20/11/2026: monitoramento de 30 produtos em cinco lojas virtuais e lojas físicas de Cuiabá; Redmi Note 15 foi encontrado na mesma semana entre R$ 1.394,00 e R$ 2.799,99. Dados regionais e datados, não preço atual nacional. Fonte: https://www5.sefaz.mt.gov.br/web/procon/w/procon-estadual-monitora-pre%C3%A7os-de-produtos-mais-vendidos-na-black-friday
- Procon-SE, relatório de fiscalização Black Friday 2026, monitoramento presencial e online em quatro semanas de novembro, incluindo 23–27/11. Fonte: https://www.se.gov.br/anexos/uploads/download/midia/484/4cc2a9bdfd93fd2d486a600a8d0ae94f.pdf

Essas fontes são sinais editoriais de comparação e transparência. Não são feed de ofertas, preço vigente de parceiro, estoque, TAG autenticada, INT.1/INT.2 ou conversão.

## 7. Integridade e decisão

- Nenhuma escrita em Render ou Neon.
- Nenhum merge, deploy, anúncio pago, gasto, publicação, clique sintético ou venda sintética.
- Wero1Operário e Wero1Elétrico não foram alterados.
- Vendas, conversões, comissões e pagamentos comprovados nesta iteração: zero.

**Decisão: HOLD.** O Render não pôde ser revalidado por falta de workspace selecionado. Neon produção continua sem tabelas públicas; staging contém histórico operacional, mas não tem backup restaurável demonstrado. O código candidato tem CI positivo, porém segue Draft e sem homologação HTTP em staging. Proveniência autenticada, catálogo elegível, publicação Metricool e atribuição por campanha permanecem bloqueados.
