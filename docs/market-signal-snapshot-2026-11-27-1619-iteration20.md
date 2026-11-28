# PARADIGMA — Snapshot operacional Iteração 20
Data: 27/11/2026 16:19 BRT
Escopo: Wero1Mercados / Wero1Divulgação
Decisão: HOLD — sem promoção para produção.

## 1. Render — Wero1Mercados produção
- Workspace: My Workspace.
- Serviço: `srv-db2fvq4s728c73cahjq0`, branch `main`, Oregon, Free, auto-deploy por commit ativo, não suspenso.
- Health Check Path vazio; nenhuma instância PostgreSQL listada na conta.
- Consulta direta ao banco `dpg-db2h93h7lnhs73ev17og-a`: 404 (not found).
- Último deploy conhecido permanece no commit `80018a1c3b4a41d8bb052ddf798b11b10d613afa`.
- Eventos de 27/11 00:00–19:20 UTC: 15 `server_failed`, todos com `nonZeroExit=3`; cinco falhas novas entre 18:44 e 18:54 UTC.
- Logs de 18:54:22 UTC mostram `psycopg.OperationalError: failed to resolve host 'dpg-db2h93h7lnhs73ev17og-a'` e `Application startup failed`.
- Métricas de CPU, memória, instâncias, HTTP e latência entre 13:20–19:20 UTC: sem séries.
- GET de `/health` não acessível pela ferramenta de leitura; não inferir status HTTP.
- Expiração informada do PostgreSQL gratuito: 05/11/2026, data já passada.

## 2. Render — staging
- Wero1Mercados staging: `srv-db6k648473hc73dkvk70`, branch `dev/p0-provider-reconciliation-20261012`, auto-deploy desligado, Health Check vazio.
- Wero1Divulgação staging: `srv-db79kdm7bikc73a1rv20`, branch `feat/wero1divulgacao-bootstrap`, auto-deploy desligado, Health Check vazio.
- Ambos sem eventos e logs entre 13:20–19:20 UTC.
- GET de `/health` e `/ready` não acessível pela ferramenta de leitura. O código de Wero1Divulgação declara uma rota /health, mas runtime não foi comprovado.
- Não há evidência de conexão Render staging → Neon staging.

## 3. Neon — produção e staging
- Produção: projeto `long-tooth-35390946`, branch `br-spring-hall-b5ed425u`, Ready, PostgreSQL 17. Zero tabelas públicas, zero snapshots e schedule vazio.
- Staging: projeto `floral-hat-53843763`, branch `br-autumn-salad-b4cg34pj`, Ready, PostgreSQL 17. 15 tabelas públicas, zero snapshots e schedule vazio.
- Quota reset informada: 01/12/2026 00:00 UTC.
- SQL read-only de staging:
  - `product_offers`: total 19; active 19; available 0; provider_verified 0; price positivo 0; commission positiva 0; source_updated_at nos últimos 7 dias 0.
  - `offers` legadas: total 20; active 19.
  - `clicks` 0; `conversions` 0; `outbound_action_tokens` 0; `affiliate_conversion_audit` 0; `affiliate_conversion_ledger` 0.
  - `ops_persistence_probe`: 59 registros. Último readback histórico: `paradigma-auto11-20261127-0917-bst`, checked_at 2026-11-27 12:27:24 UTC, finalidade operacional de staging sem evento comercial.
- Nenhuma escrita SQL nesta iteração.
- Esquema: `product_offers` não possui campos INT.1/INT.2; `outbound_action_tokens` possui `created_at`/`consumed_at`, sem `expires_at`; a candidata usa TTL de 10 minutos por `created_at`. `affiliate_conversion_audit` registra parceiro/conta/relatório/SHA-256, mas hash isolado não autentica o emissor.

## 4. GitHub — main e candidatas P0
- Repositórios consultados: `Neymaresol/wero1mercados` e `Neymaresol/Wero1all`.
- Main de Wero1Mercados ainda chama `init_db()` e seeds no startup; /health usa SELECT 1; GET /go/ grava visita; POST /out/ grava clique sem token.
- `/api/premium/ai-ranking` na main usa LEFT JOIN e ordena por cliques/7 dias, mas não tem HAVING para excluir zero cliques nem exigir clique recente. Pode retornar ofertas sem clique.
- PR #137, HEAD `d49bb705c8500acf4620482f209acc5a6ece4328`: aberta, Draft; 4/4 workflows success. Candidata exige pelo menos um clique total e um clique nos últimos 7 dias no ranking consultivo; separa esse ranking de INT; `int_qualification.filter_int_qualified_offers()` retorna lista vazia até existir pipeline de eventos autenticado.
- PR #140, HEAD `05306f2efe9af0d4fb7d147294a5bcce4c574b09`: aberta, Draft; 4/4 workflows success; `AUTHENTICATED_ADAPTER_AVAILABLE = False`; conversões manuais continuam rejeitadas.
- PR #141, HEAD `3187aea0ac32bfb4ce539c4154ddbc9e70dcbb2e`: aberta, Draft; 4/4 workflows success; vitrine direciona cartões para `/go/{offer_id}`.
- Token candidato: SHA-256 armazenado, vinculado à oferta, consumo atômico e validade de 10 minutos via `created_at`; testes offline cobrem formato, duplicidade, tamanho, replay e expiração. Prefetch explícito não registra visita/token. Token não prova identidade humana nem INT autenticada.
- PRs #137/#140/#141 permanecem Draft e não mescladas. CI usa PostgreSQL descartável; não equivale à homologação HTTP no Render.
- PR #51 de Wero1all permanece Draft. Workflow documental do HEAD anterior concluiu success.

## 5. Wero1Divulgação — código de staging
- Branch Render: `feat/wero1divulgacao-bootstrap`, código `0.4.0-dev`.
- `/api/status`: publicação false, anúncios pagos false, integrações não configuradas, catálogo bloqueado sem fonte autorizada, ranking bloqueado sem fonte autorizada.
- `/api/plan` e `/api/intent/rank` ignoram autorização declarada no payload; não aceitam flags do chamador como prova.
- `intent.py` exige TAG1 > 0 e TAG2 > 0 independentemente para ranking consultivo. TAG1/TAG2 não autenticam INT.1/INT.2.
- Nenhuma publicação ou simulação comercial executada.

## 6. Metricool — marca NeyMareSol
- Brand ID 7259526; timezone America/Sao_Paulo.
- Instagram conectado `neymaresoloficial`, divergente do destino desejado `@neymaresol`.
- Facebook conectado; TikTok conectado `neymaresoltiktok`.
- Posts agendados de 27/11 a 04/12: 0.
- Facebook feed posts 20–27/11: rows vazias.
- Instagram feed posts 20–27/11: rows vazias.
- TikTok: 25 vídeos (9 em 27/11, 2 em 25/11, 14 em 21/11); 677 views, 66 likes, 2 comentários, 0 compartilhamentos. Em 27/11: 9 vídeos, 161 views, 11 likes.
- SmartLinks timeline: rows vazias; atribuição por campanha não comprovada.
- Melhor janela seguinte consultada: sábado 28/11, 10h Facebook (score 8.850) e TikTok (score 852). Instagram retornou score zero em todos os horários. Scores relativos, não previsão de vendas.
- Nenhuma publicação ou agendamento criado.

## 7. Sinal público editorial
- Senacon/MJSP publicou em 25/11/2026 cartilha para compras on-line na Black Friday: comparar preço final com frete/taxas/juros, verificar reputação e domínio oficial, evitar falsa urgência e descontos suspeitos, confirmar destinatário Pix/boleto e guardar comprovantes.
- Fonte: https://www.gov.br/mj/pt-br/assuntos/noticias/senacon-lanca-cartilha-com-orientacoes-para-compras-seguras-na-black-friday
- Uso editorial somente; não é catálogo, INT, conversão ou prova de oferta afiliada.

## 8. Controles e gates
- Nenhuma escrita em Render ou Neon; nenhuma publicação Metricool, anúncio, gasto, clique, conversão, venda, comissão ou pagamento sintético.
- Wero1Operário e Wero1Elétrico intocados.
- Promoção bloqueada até recuperar/migrar PostgreSQL, comprovar backup+restore isolado, provar isolamento Render staging → Neon staging, homologar /health /ready /go/ /out/ em staging, integrar adapter autenticado de parceiro, consolidar Double Check e comprovar rollback.
- P2 visual/escala permanece suspenso.
