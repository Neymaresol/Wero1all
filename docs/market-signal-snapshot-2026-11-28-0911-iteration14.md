# PARADIGMA — Iteração 14
**Wero1Mercados / Wero1Divulgação — 28/11/2026, 09:11 BRT**

## Decisão
**HOLD — produção não liberada.** Inspeção read-only em GitHub, Render (My Workspace), Neon e Metricool. Escrita limitada a este relatório na branch documental da PR #51. Sem deploy, merge, publicação ou evento comercial.

## P0 — Render
- Workspace confirmado pela listagem: My Workspace.
- Produção Wero1Mercados: serviço `srv-db2fvq4s728c73cahjq0`, `main`, Free, 1 instância, auto-deploy por commit, não suspenso, health-check path vazio.
- Render não lista PostgreSQL. ID antigo `dpg-db2h93h7lnhs73ev17og-a` continua ausente; expiração informada em 05/11/2026 já passou.
- Eventos recentes: 20 `server_failed` retornados na página de 7 dias, todos exit code 3; cursor indica possível paginação adicional. Cinco eventos em 27/11 18:44–18:54 UTC. Logs de 28/11 07:30–12:30 UTC: vazio.
- Health/ready públicos não acessíveis via ferramenta HTTP; health runtime não confirmado.
- Staging Wero1Mercados: branch antiga `dev/p0-provider-reconciliation-20261012`, auto-deploy off, health-check vazio, eventos recentes vazios.
- Staging Wero1Divulgação: branch `feat/wero1divulgacao-bootstrap`, auto-deploy off, health-check vazio; último deploy Live 25/11 05:24:58 UTC, build/deploy success. Eventos retornados apenas desse deploy.

## P0 — Neon
- Produção `long-tooth-35390946`, branch main Ready: 0 tabelas públicas. Não foi executado SQL de produção nesta rodada; schema comercial não está presente.
- Staging `floral-hat-53843763`, branch main Ready: 15 tabelas públicas.
- Query read-only corrigida após descoberta do schema (colunas reais `price_brl`/`commission_brl`, probe apenas `probe_id`, `checked_at`, `purpose`):
  - `product_offers`: 19 total, 19 active, 0 available, 0 provider_verified, 0 preço positivo, 0 comissão positiva, 0 atualizadas em 7 dias.
  - Cliques, conversões, tokens outbound, auditoria, ledger, catalog visits e landing visits: todos 0.
  - `ops_persistence_probe`: 61 registros. Último: `paradigma-auto11-20261128-0011-bst`, 03:13:44 UTC (00:13:44 BRT), propósito operacional de staging, sem evento comercial.
- Snapshots/restore isolado não comprovados.

## P0 — GitHub e ranking
- Main Wero1Mercados SHA `1b17084ee04c910d19a694bf79dd4f6bb4ea4516`: `/api/premium/ai-ranking` ainda permite ofertas com zero cliques, pois LEFT JOIN não é acompanhado de HAVING de clique positivo/recente.
- PR #137 Draft HEAD `d49bb705c8500acf4620482f209acc5a6ece4328`: candidata exige ao menos 1 clique e 1 clique nos últimos 7 dias; prefetch não cria visita/token; token outbound é curto, vinculado à oferta e de uso único; startup DDL/seeds protegido por opt-in exclusivamente staging; health não declara persistência durável a partir de `SELECT 1`; INT.1/INT.2 fail-closed sem adapter autenticado.
- CI direto do HEAD #137: 4/4 workflows success (P0 Double Check, campanha, contrato comercial, PostgreSQL isolado PG17/18). CI é evidência de testes, não homologação runtime.
- PR #47 Wero1Divulgação: Draft, aberta, exige TAG1 e TAG2 positivas separadamente. PR #50: Draft, aberta, status `registered_fail_closed`. Ambas não mescladas.

## P1 — Metricool (dados corrigidos)
- Marca NeyMareSol ID 7259526; Instagram conectado `@neymaresoloficial` é diferente do alvo `@neymaresol`; Facebook e TikTok conectados.
- Agendamentos 28/11–05/12: 0.
- TikTok, 21–28/11, consulta com IDs válidos do catálogo (`TKPO07–TKPO11`): 25 vídeos; 677 views; 66 likes; 2 comentários; 0 shares; reach não retornado (null).
- Instagram posts e Facebook posts: nenhuma linha retornada no período (não é prova de ausência de publicação).
- Melhores horários de sábado: Facebook 10h score 8.850; TikTok 10h score 852. Instagram scores zero. Scores são relativos, não previsões de vendas.
- Nenhuma publicação, agendamento, anúncio ou campanha criada. Atribuição não disponível.

## Integridade financeira
Vendas comprovadas: 0; conversões: 0; comissões: R$ 0,00; pagamentos: R$ 0,00.

## Gates
1. Recuperar/migrar PostgreSQL de produção e comprovar Render→Neon.
2. Backup/restauração isolada.
3. Confirmar isolamento staging.
4. Homologar /health, /ready, /go/ e /out/ sem eventos comerciais sintéticos.
5. Adapter de parceiro autenticado.
6. Double Check combinado e rollback.
7. Só então avaliar promoção. P2 visual/escala permanece adiada.

Nenhuma alteração Render/Neon, deploy, merge, anúncio, gasto, publicação, clique, conversão, venda sintética ou pagamento nesta rodada. Wero1Operário e Wero1Elétrico permanecem intocados.
