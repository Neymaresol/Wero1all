# PARADIGMA — Snapshot operacional Iteração 19
Data: 27/11/2026 15:17 BRT
Escopo: Wero1Mercados / Wero1Divulgação
Decisão: HOLD — sem promoção para produção.

## 1. Render — Wero1Mercados produção
- Workspace consultado: My Workspace.
- Serviço: `srv-db2fvq4s728c73cahjq0`, branch `main`, Oregon, plano Free, auto-deploy por commit ativo, não suspenso.
- Health Check Path vazio.
- A conta lista zero instâncias PostgreSQL.
- Consulta direta ao banco `dpg-db2h93h7lnhs73ev17og-a` retorna 404.
- Último deploy Live: 23/10/2026, commit `80018a1c3b4a41d8bb052ddf798b11b10d613afa`.
- Eventos na janela de 24h: 10 `server_failed`, todos `nonZeroExit=3`; mais recente em 27/11 04:19 UTC (01:19 BRT).
- Logs de 27/11 12:00–18:17 UTC: vazios; métricas CPU, memória, instâncias, HTTP e latência: sem séries.
- GET de /health não pôde ser validado pela ferramenta de leitura web; não inferir status HTTP.
- Expiração informada do Postgres gratuito: 05/11/2026, data já passada.

## 2. Render — staging
- Wero1Mercados staging: `srv-db6k648473hc73dkvk70`, branch `dev/p0-provider-reconciliation-20261012`, auto-deploy desligado, Health Check vazio. Último deploy Live em 13/10/2026, commit `9a3741d30f18d172b2cacc147427b686100694a4`.
- Wero1Divulgação staging: `srv-db79kdm7bikc73a1rv20`, branch `feat/wero1divulgacao-bootstrap`, auto-deploy desligado, Health Check vazio. Último deploy Live em 25/11/2026, commit `e07b255cd6dd400ee418a8747ad19446723ce430`.
- Ambos: sem eventos, logs e séries de métricas na janela consultada de 24h/6h.
- Abertura web de /health dos dois serviços não foi acessível; isso não comprova falha nem sucesso de runtime.

## 3. Neon — produção e staging
- Produção: projeto `long-tooth-35390946`, branch `br-spring-hall-b5ed425u`, Ready, PostgreSQL 17, região AWS us-east-2. Zero tabelas públicas, zero snapshots e schedule vazio.
- Staging: projeto `floral-hat-53843763`, branch `br-autumn-salad-b4cg34pj`, Ready, PostgreSQL 17, região AWS us-east-2. 15 tabelas públicas, zero snapshots e schedule vazio.
- Quota reset informada: 01/12/2026 00:00 UTC.
- SQL read-only de staging:
  - product_offers: total 19; active 19; available 0; provider_verified 0; preço positivo 0; comissão positiva 0; source_updated_at nos últimos 7 dias 0.
  - offers legadas 20; clicks 0; conversions 0; outbound_action_tokens 0; affiliate_conversion_audit 0; affiliate_conversion_ledger 0; ops_persistence_probe 59.
- Nenhuma escrita SQL nesta iteração.
- Esquema: product_offers usa active/available/price_brl/commission_brl e não possui INT.1/INT.2; clicks e conversions referenciam offers; outbound_action_tokens possui created_at/consumed_at, sem expires_at; affiliate_conversion_audit guarda source_partner/account/report/SHA-256, mas hash isolado não autentica o emissor.
- Não há backup restaurável comprovado nem vínculo Render staging → Neon staging comprovado.

## 4. GitHub — código e Double Check
- Repositórios públicos consultados: Neymaresol/wero1mercados e Neymaresol/Wero1all.
- Main de Wero1Mercados:
  - startup() chama init_db() e seeds;
  - /health deriva storage_persistent de SELECT 1;
  - GET /go/{offer_id} grava offer_landing_visits;
  - POST /out/{offer_id} grava clicks sem token de ação;
  - premium_ai_ranking usa LEFT JOIN e não filtra COUNT(c.id)>0 nem clique recente.
  - Conversão manual exige admin mas falha fechada por ausência de adapter autenticado.
- PR #137, HEAD `d49bb705c8500acf4620482f209acc5a6ece4328`: aberta, Draft; 4/4 workflows PR concluídos com success (P0 Double Check, campaign checks, Commercial Contract Double Check, PostgreSQL 17/18).
- PR #140, HEAD `05306f2efe9af0d4fb7d147294a5bcce4c574b09`: aberta, Draft; 4/4 workflows success; mantém conversões bloqueadas até adapter autenticado.
- PR #141, HEAD `3187aea0ac32bfb4ce539c4154ddbc9e70dcbb2e`: aberta, Draft; 4/4 workflows success; vitrine passa a usar /go/.
- #137 separa INT.1/INT.2 de cliques e mantém a fila INT vazia até existir pipeline de eventos autenticado. CI usa PostgreSQL descartável, não homologação Render.
- Nenhuma PR mesclada. Nenhum deploy ou escrita em produção.

## 5. Metricool — marca NeyMareSol
- Brand ID 7259526, timezone America/Sao_Paulo.
- Instagram conectado `neymaresoloficial`, divergente do destino desejado `@neymaresol`.
- Facebook conectado (ID 102552892426549); TikTok conectado (`neymaresoltiktok`).
- Posts agendados entre 27/11 15:17 e 04/12 23:59 BRT: 0.
- Facebook feed posts: rows vazias; Instagram feed posts: rows vazias; SmartLinks timeline: rows vazias.
- Evolution 20–27/11: Facebook 2 seguidores nos snapshots; Instagram 45; TikTok 25 vídeos, 677 views, 66 likes, 2 comentários, 0 compartilhamentos; último snapshot de seguidores TikTok 6.091 (26/11).
- Próxima janela útil sugerida para sábado 28/11: 10h Facebook (score 8.850) e 10h TikTok (score 852). Scores são indicadores internos do Metricool, não previsão de vendas.
- Nenhuma publicação ou agendamento criado; atribuição por campanha não comprovada.

## 6. Sinal público editorial
- Senacon/MJSP, cartilha publicada em 25/11/2026: comparar preço final com frete, taxas e juros; conferir reputação e domínio oficial; desconfiar de desconto excessivo/urgência artificial; validar destinatário Pix/boleto; guardar comprovantes e registros.
- Fonte: https://www.gov.br/mj/pt-br/assuntos/noticias/senacon-lanca-cartilha-com-orientacoes-para-compras-seguras-na-black-friday
- Uso apenas editorial; não autentica catálogo, INT, clique ou conversão.

## 7. Controles e gates
- Nenhuma escrita em Render ou Neon; nenhuma publicação Metricool, anúncio, gasto, clique, conversão, venda, comissão ou pagamento sintético.
- Wero1Operário e Wero1Elétrico intocados.
- Promoção bloqueada até recuperar/migrar Postgres, comprovar backup+restore isolado, provar isolamento Render staging → Neon staging, homologar /health /ready /go/ /out/ em staging, integrar adapter autenticado de parceiro, consolidar Double Check e comprovar rollback.
- P2 visual/escala permanece suspenso.
