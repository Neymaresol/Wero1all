# PARADIGMA — Iteração 23 (27/11/2026, 19:18–19:21 BRT)

## Decisão
**HOLD — não promover produção.** Nenhum deploy, merge, publicação, anúncio, clique, conversão ou pagamento foi criado nesta execução.

## P0 — Render
- Workspace confirmado: My Workspace.
- Produção `wero1mercados` (`srv-db2fvq4s728c73cahjq0`): branch `main`, Free/Oregon, auto-deploy ligado, serviço não suspenso, Health Check Path vazio.
- Render lista zero instâncias PostgreSQL. Consulta ao ID legado `dpg-db2h93h7lnhs73ev17og-a` retorna 404.
- Último deploy Live listado: 23/10/2026, commit `80018a1c3b4a41d8bb052ddf798b11b10d613afa`.
- Na janela 18:00–22:20 UTC de 27/11: cinco eventos `server_failed`, exit code 3, entre 18:44 e 18:54 UTC. Log de 18:54 confirma falha DNS ao resolver o hostname PostgreSQL legado e `Application startup failed`.
- CPU, memória, instâncias, HTTP e latência sem séries. Health HTTP não comprovado.
- Wero1Mercados staging (`srv-db6k648473hc73dkvk70)): branch antiga `dev/p0-provider-reconciliation-20261012`, auto-deploy desligado, Health Check vazio, último deploy Live 13/10/2026; nenhum evento de 20–27/11.
- Wero1Divulgação staging (`srv-db79kdm7bikc73a1rv20`): branch `feat/wero1divulgacao-bootstrap`, auto-deploy desligado, Health Check vazio; último deploy Live bem-sucedido em 25/11/2026, commit `e07b255cd6dd400ee418a8747ad19446723ce430`.
- GET de `/health` e `/api/status` nos hosts de staging não ficou acessível pela ferramenta web; isso não comprova indisponibilidade. Não foram chamadas rotas comerciais.

## P0 — Neon
- Produção: projeto `long-tooth-35390946`, branch `br-spring-hall-b5ed425u` Ready, banco `neondb`, schema público vazio, compute idle, 0 snapshots e schedule vazio.
- Staging: projeto `floral-hat-53843763`, branch `br-autumn-salad-b4cg34pj` Ready, 15 tabelas públicas, compute idle/suspenso após a última atividade, 0 snapshots e schedule vazio.
- O último probe operacional existente em staging é `paradigma-auto11-20261127-1814-bst`, registrado às 18:19:21 BRT. Readback confirmou `probe_id`, `checked_at` e propósito explicitamente não comercial. Nenhum novo probe foi gravado nesta iteração.
- SQL SELECT em staging: product_offers=19; offers=20; clicks=0; conversions=0; outbound_action_tokens=0; affiliate_conversion_audit=0; affiliate_conversion_ledger=0; ops_persistence_probe=60; catalog_visits=0; offer_landing_visits=0.
- Elegibilidade de product_offers: 19 ativas, 0 disponíveis, 0 provider_verified, 0 com preço positivo, 0 com comissão positiva e 0 atualizadas nos últimos sete dias.
- O nome real do ledger é `affiliate_conversion_ledger` (não `commission_ledger`).
- `product_offers` não possui colunas INT.1/INT.2. `outbound_action_tokens` possui `created_at` e `consumed_at`, mas não `expires_at`; a PR candidata aplica TTL de dez minutos pela condição de `created_at`.
- `conversions` possui ID externo único e valores/status, mas a tabela isolada não autentica a origem do parceiro. O audit/ledger guardam parceiro, conta, relatório e SHA-256; hash isolado não comprova assinatura/identidade do emissor.
- Quota reset Neon informado: 01/12/2026 00:00 UTC. Não confundir com a expiração informada em 05/11/2026 do PostgreSQL Free antigo do Render, já ultrapassada.

## P0 — GitHub, ranking e funil
- A versão `main` de `Neymaresol/wero1mercados` ainda contém ranking com LEFT JOIN sem HAVING para excluir zero cliques/atividade antiga, startup chamando `init_db()`, health baseado em `SELECT 1` e rota legada Amazon GET que grava clique.
- PR #137 (HEAD `d49bb705c8500acf4620482f209acc5a6ece4328`): Draft/open; 4 workflows concluídos com success. Corrige ranking consultivo para clique positivo e recente, mantém INT fail-closed, protege prefetch em `/go/`, exige token único em POST `/out/`, e remove DDL/seeds automáticos por padrão.
- PR #140 (HEAD `05306f2efe9af0d4fb7d147294a5bcce4c574b09`): Draft/open; 4 workflows success. Adapter autenticado permanece explicitamente indisponível; conversões não autenticadas continuam rejeitadas.
- PR #141 (HEAD `3187aea0ac32bfb4ce539c4154ddbc9e70dcbb2e`): Draft/open; 4 workflows success. Vitrine candidata direciona para `/go/{offer_id}` e remove clique do GET legado.
- Status-checks combinados retornaram listas vazias; a evidência positiva é dos workflow runs acima. CI usa PostgreSQL descartável e não substitui homologação HTTP no Render.
- PR #137/#140/#141 não foram mescladas. `/go/` e `/out/` não foram exercitadas em runtime: não foi gerado clique sintético nem ação de saída.

## P1 — Wero1Divulgação
- Branch staging `feat/wero1divulgacao-bootstrap`, código `0.4.0-dev`.
- `/health` no código é estático; runtime não comprovado.
- `/api/status` e `/api/plan` mantêm publicação e planejamento bloqueados sem catálogo autorizado server-side.
- `/api/intent/rank` bloqueia sinais enviados pelo chamador; caller-supplied não autentica INT.1/INT.2.
- PR #47: TAG1 e TAG2 precisam ser positivas independentemente; 2 workflows success; Draft.
- PR #50: status de ranking explicitamente fail-closed; 2 workflows success; Draft.
- Nenhum adapter público/autorizado de catálogo ou sinais foi integrado; nenhum post foi publicado.

## P1 — Metricool
- Marca NeyMareSol, brandId 7259526, timezone America/Sao_Paulo.
- Instagram conectado `@neymaresoloficial`; conta desejada `@neymaresol`: divergência confirmada.
- Facebook conectado; TikTok conectado como `neymaresoltiktok`.
- Posts agendados de 27/11 a 05/12: 0.
- Analytics 20–27/11: Facebook sem linhas retornadas; Instagram sem linhas; SmartLinks sem linhas.
- TikTok: 25 posts, 677 views, 66 likes, 2 comentários e 0 compartilhamentos; 14 posts em 21/11, 2 em 25/11 e 9 em 27/11.
- Melhor horário retornado para sábado 28/11: Facebook 10h (score 8.850); TikTok 10h (852); Instagram scores 0. Scores são relativos, não previsão de vendas.
- Atribuição por campanha não comprovada. Nenhum post criado/agendado.

## Sinais públicos para pauta editorial
- Procon-MT, 20/11/2026: monitorou 30 produtos em cinco lojas virtuais e comércio físico de Cuiabá; 262 preços online e 438 presenciais. Na Amazon, OMO líquido 3L subiu 54% numa semana (R$ 36,99 para R$ 56,90) e geladeira Brastemp 375L subiu 22% (R$ 2.717,10 para R$ 3.310,75). Dados regionais/históricos, não preços atuais nacionais.
  Fonte: https://www5.sefaz.mt.gov.br/web/procon/w/procon-estadual-monitora-precos-de-produtos-mais-vendidos-na-black-friday
- Senacon/MJSP, 25/11/2026: comparar preço total com frete, taxas e juros; verificar reputação e domínio do vendedor; evitar falsa urgência; conferir destinatário Pix/boleto e guardar comprovantes.
  Fonte: https://www.gov.br/mj/pt-br/assuntos/noticias/senacon-lanca-cartilha-com-orientacoes-para-compras-seguras-na-black-friday
- Sinais servem apenas para conteúdo educativo; não são ofertas afiliadas, dados de catálogo, intenção autenticada ou conversões.

## Integridade e promoção
- Nenhuma escrita em Render ou Neon nesta iteração; somente SELECT no Neon staging.
- Nenhum merge, deploy, publicação, anúncio pago, gasto, clique, conversão, venda, comissão ou pagamento sintético.
- Wero1Operário e Wero1Elétrico não foram alterados.
- Próximos gates: restaurar/migrar PostgreSQL de produção; provar backup/restore isolado; provar conexão exclusiva Render staging→Neon staging; adapter parceiro com autenticação server-side, assinatura, conta, replay e idempotência; homologar health/ready/go/out no staging; Double Check integrado e rollback comprovado.
