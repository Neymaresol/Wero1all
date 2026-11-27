# PARADIGMA — Iteração 24
**Data da inspeção:** 27/11/2026, 20:18 BRT  
**Escopo:** Wero1Mercados / Wero1Divulgação  
**Decisão:** HOLD — sem promoção de produção

## 1. Render — produção

Serviço `wero1mercados`, ID `srv-db2fvq4s728c73cahjq0`:
- `main`, plano Free, Oregon; auto-deploy por commit ativo; serviço não suspenso.
- Health Check Path vazio; 1 instância configurada; último update de configuração retornado: 23/10/2026.
- Banco solicitado `dpg-db2h93h7lnhs73ev17og-a`: consulta direta `get_postgres` retornou HTTP 404.
- Eventos de 27/11: 15 `server_failed`, todos com `nonZeroExit=3`; último em 18:54:24 UTC (15:54:24 BRT).
- Consulta de logs, métricas e listagem de Postgres do workspace não foi concluída: a API exige workspace selecionado e a execução não selecionou workspace sem confirmação específica. Portanto, não há leitura nova de log/CPU/memória/HTTP nesta rodada.
- Health HTTP não foi testado com sucesso; estado runtime permanece NÃO COMPROVADO.

A data de expiração informada anteriormente (05/11/2026) já passou. Não houve reinício, alteração de configuração, deploy ou escrita em produção.

## 2. Render — staging

- Wero1Mercados staging: `srv-db6k648473hc73dkvk70`, branch `dev/p0-provider-reconciliation-20261012`, auto-deploy desligado, Free/Oregon, health path vazio.
- Wero1Divulgação staging: `srv-db79kdm7bikc73a1rv20`, branch `feat/wero1divulgacao-bootstrap`, auto-deploy desligado, Free/Oregon, health path vazio.
- Não foi comprovada conexão HTTP/runtime dos serviços com Neon staging.

## 3. Neon — produção e staging

### Produção
Projeto `long-tooth-35390946` (`wero1mercados-production`), PostgreSQL 17, região AWS us-east-2:
- 0 tabelas públicas no banco consultado.
- 0 snapshots.
- Quota reset indicada para 01/12/2026 00:00 UTC.
- O compute tinha atividade registrada em 27/11 às 22:20 UTC; isso não prova persistência comercial.

### Staging
Projeto `floral-hat-53843763`, branch `br-autumn-salad-b4cg34pj`, estado Ready, PostgreSQL 17:
- 15 tabelas públicas.
- 0 snapshots; schedule automático vazio.
- SQL read-only: 19 product_offers, 19 ativas, 0 disponíveis, 0 provider_verified, 0 com preço positivo, 0 com comissão positiva, 0 atualizadas em 7 dias, 20 ofertas legadas.
- 0 cliques, 0 conversões, 0 tokens outbound, 0 auditorias, 0 linhas no affiliate_conversion_ledger, 0 visitas ao catálogo.
- 60 probes operacionais. Último: `paradigma-auto11-20261127-1814-bst`, checked_at 21:19:21 UTC (18:19:21 BRT), finalidade operacional sem evento comercial.

Colunas confirmadas:
- `product_offers.provider_verified` existe; não há colunas INT.1/INT.2.
- `outbound_action_tokens` tem `created_at` e `consumed_at`, sem `expires_at`.
- Conversões/auditoria/ledger possuem identificadores e metadados de relatório/hash; hash isolado não autentica o emissor.

Nenhuma escrita SQL foi realizada nesta iteração.

## 4. GitHub — produção versus candidatas

### Main de Wero1Mercados
Arquivo `main.py`, versão declarada `1.14.15-BR-rc1`, ainda contém:
- Startup chama `init_db()` e seeds.
- `/health` usa `SELECT 1` e declara `storage_persistent` com base apenas em conectividade.
- GET `/go/{offer_id}` grava `offer_landing_visits`.
- POST `/out/{offer_id}` grava clique sem token de uso único.
- Ranking `/api/premium/ai-ranking` usa LEFT JOIN e não tem HAVING para excluir ofertas sem clique/atividade recente.

### Candidatas isoladas
- PR #137: open/Draft; HEAD `d49bb705c8500acf4620482f209acc5a6ece4328`. Quatro workflows concluídos com success (PARADIGMA P0, Wero1 campaign checks, PostgreSQL PG17/PG18 e Commercial Contract).
- PR #140: open/Draft; HEAD `05306f2efe9af0d4fb7d147294a5bcce4c574b09`. Quatro workflows concluídos com success; adapter autenticado permanece explicitamente indisponível e conversões continuam fail-closed.
- PR #141: open/Draft; HEAD `3187aea0ac32bfb4ce539c4154ddbc9e70dcbb2e`. Quatro workflows concluídos com success; vitrine candidata aponta para /go/.
- Os status checks combinados retornaram lista vazia; a evidência de CI desta rodada é a lista de workflow runs concluídos com success, não status checks combinados.
- A branch candidata #137 foi inspecionada: startup sem DDL/seeds por padrão, health não afirma persistência com SELECT 1, prefetch de /go/ retorna 204 sem token/visita, /out/ consome token de uso único vinculado à oferta com janela de 10 minutos, e ranking exige clique positivo e recente. Cliques seguem consultivos, não INT.

### Wero1Divulgação
- PR #47: open/Draft; dois workflows Double Check concluídos com success; exige TAG1 > 0 e TAG2 > 0 separadamente.
- PR #50: open/Draft; dois workflows Double Check concluídos com success; status do ranking é explicitamente `registered_fail_closed`.
- PR #51 documental permanece open/Draft. Nenhum merge foi realizado.

Nenhuma PR foi mesclada; nenhuma implantação foi executada.

## 5. Metricool — marca NeyMareSol (7259526)

Configuração retornada:
- Timezone: America/Sao_Paulo.
- Instagram conectado: `neymaresoloficial`; alvo informado para o projeto: `@neymaresol` — divergência confirmada.
- Facebook conectado (ID 102552892426549).
- TikTok conectado (`neymaresoltiktok`).

Janela analítica 20–27/11:
- Facebook posts: 0 linhas retornadas.
- Instagram posts: 0 linhas retornadas.
- TikTok: 25 vídeos; 677 visualizações, 66 likes, 2 comentários, 0 compartilhamentos. Por data: 21/11 (14 vídeos, 403 views), 25/11 (2, 113), 27/11 (9, 161).
- SmartLinks timeline: 0 linhas.
- Posts agendados de 27/11 20:18 a 04/12 23:59 BRT: 0.

Melhores scores relativos para sábado 28/11: Facebook 10h = 8.850; TikTok 10h = 852; Instagram = 0 em todas as horas. Scores não são previsão de vendas. Nenhuma publicação foi criada/agendada; atribuição por campanha não comprovada.

## 6. Sinais públicos autorizados — uso editorial

- Procon-ES, pesquisa publicada em 18/11 e atualizada em 26/11: mais de 40 produtos analisados; diferenças de preços chegaram a 230%. Orientação: comparar histórico e condições, não apenas percentual de desconto. Fonte: https://procon.es.gov.br/black-friday-pesquisa-do-procon-es-identifica-variacao-de-ate-230-nos-precos-de-produtos
- Senacon/MJSP, cartilha publicada em 25/11: conferir preço total, frete, taxas, juros, reputação e domínio da loja; verificar destinatário de Pix/boleto; preservar comprovantes e desconfiar de descontos excessivos. Fonte: https://www.gov.br/mj/pt-br/assuntos/noticias/senacon-lanca-cartilha-com-orientacoes-para-compras-seguras-na-black-friday

Os sinais são pauta educativa, não catálogo afiliado, preço atual de oferta, INT.1/INT.2 ou evidência de conversão.

## 7. Integridade e próximos gates

- Financeiro comprovado nesta iteração: nenhuma venda, conversão, comissão ou pagamento.
- Nenhuma escrita em Render ou Neon; nenhuma publicação Metricool; nenhum anúncio, gasto ou evento comercial sintético.
- Nenhuma alteração em Wero1Operário ou Wero1Elétrico.
- Única mudança planejada nesta iteração: documentação nesta branch isolada.

Gates: recuperar/migrar PostgreSQL de produção; backup restaurável e restore isolado; provar Render staging → Neon staging; integrar adapter de parceiro com autenticação de origem/conta/relatório/assinatura e anti-replay/idempotência; homologar /health, /ready, /go/ e /out/ em staging; Double Check integrado e rollback comprovado antes de qualquer promoção.

**Status final: HOLD.**
