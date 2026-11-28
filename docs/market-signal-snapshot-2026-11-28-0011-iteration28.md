# PARADIGMA — Iteração 28 (2026-11-28)

**Janela da auditoria:** 2026-11-28 00:11–00:14 BRT (03:11–03:14 UTC)  
**Decisão:** HOLD — nenhuma promoção de produção autorizada.

## 1. Render — produção Wero1Mercados

Workspace My Workspace confirmado.

- Serviço: `wero1mercados` (`srv-db2fvq4s728c73cahjq0`), branch `main`, plano Free, região Oregon.
- Serviço não suspenso; auto-deploy por commit ativo.
- Health Check Path vazio.
- Último deploy Live: 2026-10-23, commit `80018a1c3b4a41d8bb052ddf798b11b10d613afa`.
- Inventário Render: nenhum PostgreSQL.
- Consulta direta de `dpg-db2h93h7lnhs73ev17og-a`: 404 Not Found.
- A expiração informada em 2026-11-05 já passou.

Eventos na janela de 24h: 10 `server_failed`, todos com exit code 3. A paginação seguinte não retornou eventos adicionais. Logs repetem falha em `startup() → init_db() → psycopg.connect()`; erro literal: `failed to resolve host 'dpg-db2h93h7lnhs73ev17og-a'`. Última falha: 2026-11-27 18:54:24 UTC (15:54:24 BRT). Não houve eventos posteriores até o fim da janela consultada.

Métricas de CPU, memória, instâncias, HTTP request count e latência: séries vazias. Health runtime de produção não comprovado.

## 2. Render — staging

- Wero1Mercados staging: branch antiga `dev/p0-provider-reconciliation-20261012`, auto-deploy desligado, Health Check Path vazio; último deploy Live em 2026-10-13.
- Wero1Divulgação staging: branch `feat/wero1divulgacao-bootstrap`, auto-deploy desligado, Health Check Path vazio; último deploy Live em 2026-11-25, build e deploy concluídos com sucesso.
- Nenhuma branch candidata foi implantada. Tentativas de leitura HTTP pública de `/health`, `/ready` e `/api/status` não foram acessíveis pelo mecanismo de inspeção; não se declara health runtime aprovado.

## 3. Neon — produção e staging

### Produção

Projeto `wero1mercados-production` (`long-tooth-35390946`), PostgreSQL 17, região AWS us-east-2. Branch principal `main` Ready, mas sem tabelas públicas. Snapshots: 0. Agendamento de snapshots: vazio. Quota reset: 2026-12-01 00:00 UTC.

### Staging

Projeto `wero1mercados-staging` (`floral-hat-53843763`), branch principal `br-autumn-salad-b4cg34pj` Ready, PostgreSQL 17, 15 tabelas públicas. Snapshots: 0. Agendamento de snapshots: vazio.

Contagens SQL read-only antes do probe operacional:
- `product_offers`: 19; ativas 19; disponíveis 0; provider_verified 0; preço positivo 0; comissão positiva 0; atualizadas em 7 dias 0.
- `offers`: 20; ativas 19; preço positivo 0; comissão positiva 0; atualizadas em 7 dias 0.
- `partners`: 2; ativos 1.
- Cliques 0; conversões 0; tokens outbound 0; auditorias de conversão 0; ledger 0; visitas ao catálogo 0; visitas de landing 0.

### Probe operacional isolado

Foi gravado **somente** um registro em `ops_persistence_probe`, no staging, e lido novamente por uma segunda consulta SQL:

- ID: `paradigma-auto11-20261128-0011-bst`
- Timestamp: 2026-11-28 03:13:44.558 UTC
- Finalidade: verificação operacional de persistência; explicitamente sem evento comercial, clique, conversão, venda, comissão ou pagamento.
- Total de probes após o readback: 61.
- Rechecagem após o probe: cliques 0, conversões 0, tokens 0, auditorias 0, ledger 0, visitas de catálogo 0 e visitas de landing 0.

Esse readback confirma a gravação e leitura no Neon staging; não prova backup restaurável nem conexão Render staging → Neon staging. Nenhuma escrita foi feita em produção ou nas tabelas comerciais.

## 4. GitHub — código, PRs e Double Check

Repositórios `Neymaresol/wero1mercados` e `Neymaresol/Wero1all` acessíveis; branches padrão `main`.

### Wero1Mercados

- PR #137 — HEAD `d49bb705c8500acf4620482f209acc5a6ece4328`, aberta, Draft, não mesclada. Quatro workflows concluídos com success: PARADIGMA P0 Double Check, Wero1 campaign checks, P0 Isolated PostgreSQL Double Check (PG17/PG18) e P0 Commercial Contract Double Check.
- PR #140 — HEAD `05306f2efe9af0d4fb7d147294a5bcce4c574b09`, aberta, Draft, não mesclada. Quatro workflows concluídos com success.
- PR #141 — HEAD `3187aea0ac32bfb4ce539c4154ddbc9e70dcbb2e`, aberta, Draft, não mesclada. Quatro workflows concluídos com success.

Revisão dos patches:
- #137: INT.1/INT.2 fail-closed; ranking consultivo exige clique positivo e clique nos últimos sete dias; `/go/{offer_id}` não insere clique, bloqueia prefetch declarado, emite token de uso único vinculado à oferta; `/out/{offer_id}` consome token de até 10 minutos e grava clique atomicamente; health distingue reachability de persistência durável; startup DDL/seeds depende de opt-in explícito e exclusivo de staging.
- #140: `AUTHENTICATED_ADAPTER_AVAILABLE = False`; relatório manual continua rejeitado. Não há adapter autenticado de parceiro integrado.
- #141: cards da Werozinha passam a usar `/go/{offer_id}`; endpoint GET legado apenas redireciona e não contabiliza clique.

### Wero1Divulgação

- PR #47 — HEAD `e4d47ecdf101b3184db8d8660b02bb2de107873c`, aberta, Draft; dois workflows success. TAG1 e TAG2 precisam ser positivas independentemente; sinais continuam `caller_supplied`, não autenticam intenção.
- PR #50 — HEAD `b8203686def6e9036a19425f7dec135b0d0cb6f5`, aberta, Draft; dois workflows success. Status de ranking explicitamente `registered_fail_closed`.

### Documentação

PR #51 continua aberta e Draft. HEAD observado: `e03596cc1b4b6eed2f7dca73f18ab31f5983120d`. Workflow PARADIGMA P0 Double Check concluído com success; combined status retornou lista vazia. Nenhuma PR foi mesclada.

Os workflows de CI aprovados são evidência de testes automatizados em ambiente isolado; não substituem homologação HTTP em Render staging, backup/restore ou rollback real.

## 5. Metricool — marca NeyMareSol

Brand ID `7259526`, fuso `America/Sao_Paulo`.

- Instagram conectado: `@neymaresoloficial`; identidade desejada: `@neymaresol` — divergência confirmada.
- Página Facebook identificada como `Neymaresolface`.
- TikTok conectado como `neymaresoltiktok`.
- Publicações agendadas de 28/11 a 05/12: 0.
- Analytics de posts Facebook e Instagram de 21/11 a 28/11: sem linhas retornadas.
- TikTok: 25 vídeos retornados; 677 visualizações, 66 likes, 2 comentários, 0 compartilhamentos.
- SmartLinks timeline: sem linhas retornadas.
- Melhores horários relativos para sábado: Facebook 10h (score 8.850), TikTok 10h (score 852); Instagram sem score positivo (0).

Scores são recomendações relativas do Metricool, não previsões de vendas. Nenhuma publicação ou agendamento foi criado; nenhuma atribuição de campanha foi comprovada.

## 6. Sinais públicos autorizados — uso editorial

- Senacon/MJSP, 2026-11-25: cartilha recomenda comparar preço final, frete, taxas e juros; verificar reputação e domínio da loja; conferir destinatário de Pix/boleto; evitar falsa urgência e guardar comprovantes. https://www.gov.br/mj/pt-br/assuntos/noticias/senacon-lanca-cartilha-com-orientacoes-para-compras-seguras-na-black-friday
- Procon-ES, atualizado em 2026-11-26: pesquisa de mais de 40 produtos encontrou variações de até 230% entre estabelecimentos. É referência regional e temporal, não preço atual nacional. https://procon.es.gov.br/black-friday-pesquisa-do-procon-es-identifica-variacao-de-ate-230-nos-precos-de-produtos
- Anvisa, 2026-11-27: cartilha “Tá na Internet. Tá na Anvisa?” orienta consumidores e criadores de conteúdo sobre regularização e publicidade de medicamentos, suplementos, cosméticos, produtos de limpeza e dispositivos médicos. https://www.gov.br/anvisa/pt-br/assuntos/noticias-anvisa/2026/black-friday-anvisa-lanca-cartilha-digital-para-compras-seguras-na-internet

Essas fontes servem apenas para pauta educativa. Não foram transformadas em ofertas, sinais INT, catálogo afiliado ou conversões.

## 7. Integridade e decisão

- Vendas, conversões, comissões e pagamentos comprovados nesta execução: 0.
- Única escrita em banco: um probe operacional no Neon staging, com readback separado.
- Escritas comerciais: nenhuma.
- Render produção: nenhuma escrita, restart, deploy ou alteração.
- GitHub: somente documentação em branch isolada; sem merge.
- Metricool: nenhuma publicação ou agendamento.
- Nenhum anúncio pago, gasto ou evento comercial sintético.
- Wero1Operário e Wero1Elétrico permaneceram intocados.

**HOLD.** Bloqueios de promoção: recuperar/migrar PostgreSQL de produção; comprovar backup restaurável e restore isolado; provar conexão Render staging → Neon staging; implantar a candidata apenas em staging isolado; homologar `/health`, `/ready`, `/go/` e `/out/` sem contaminar métricas comerciais; integrar adapter de parceiro com autenticação server-side, assinatura, replay/uniqueness e idempotência; executar Double Check integrado e rollback comprovado.
