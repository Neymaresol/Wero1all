# PARADIGMA — Iteração 15
**Wero1Mercados / Wero1Divulgação · 28/11/2026 · 10:14 BRT**

## Decisão
**HOLD — produção não liberada.** Esta rodada foi de auditoria read-only, sem deploy, merge, alteração de banco, tráfego comercial sintético ou publicação. A conectividade do Neon de produção foi confirmada, mas seu schema comercial está vazio e Render não lista PostgreSQL.

## 🔴 P0 — Render produção
- Serviço `srv-db2fvq4s728c73cahjq0`, `wero1mercados`: `main`, Free, Oregon, auto-deploy ativo, uma instância, não suspenso, Health Check Path vazio.
- URL: https://wero1mercados.onrender.com
- PostgreSQL: **nenhuma instância encontrada** no workspace. O ID antigo `dpg-db2h93h7lnhs73ev17og-a` não existe na listagem; expiração informada em 05/11/2026 já passou.
- 20 eventos `server_failed` na página consultada, todos exit code 3; há cursor para eventos mais antigos. Cinco eventos de 27/11 entre 18:44 e 18:54 UTC (15:44–15:54 BRT) estão dentro das 24 horas desta consulta.
- Logs 28/11 12:00–13:15 UTC: 0 linhas.
- CPU, memória, instâncias, requisições e latência no mesmo intervalo: séries vazias.
- GET `/health` e `/ready` não foram acessíveis pela ferramenta HTTP. Health runtime não confirmado.

## 🔴 P0 — Neon produção e staging
**Produção** — projeto `long-tooth-35390946`, branch `br-spring-hall-b5ed425u`:
- SQL read-only `SELECT current_database(), now()` funcionou; database `neondb`.
- PostgreSQL 17, branch Ready.
- Tabelas fora dos schemas de sistema: **0**.
- Snapshots: **0**; schedule automático: **vazio**.
- Contadores atuais de armazenamento/escrita retornados como 0; não equivalem a uma prova de backup/restauração.

**Staging** — projeto `floral-hat-53843763`, branch `br-autumn-salad-b4cg34pj`:
- 15 tabelas públicas.
- `product_offers`: 19 total e ativas; 0 disponíveis, 0 provider_verified, 0 com preço positivo, 0 com comissão positiva e 0 atualizadas em 7 dias.
- `clicks`, `conversions`, `outbound_action_tokens`, `affiliate_conversion_audit`, `affiliate_conversion_ledger`, `catalog_visits`, `offer_landing_visits`: 0 cada.
- `ops_persistence_probe`: 61 registros. Último readback: `paradigma-auto11-20261128-0011-bst`, 03:13:44 UTC (00:13:44 BRT), finalidade operacional de staging, sem evento comercial.
- Snapshots e schedule automático: 0.

## 🛡️ P0 — Código main e funil
SHA de `main.py`: `1b17084ee04c910d19a694bf79dd4f6bb4ea4516`.
Defeitos confirmados no código:
1. `/api/premium/ai-ranking` ordena por cliques recentes/totais, mas não filtra clique positivo ou recente; ofertas com 0 cliques continuam no ranking.
2. Health retorna `storage_persistent=database_ok` após `SELECT 1`; conectividade SQL não comprova persistência durável.
3. GET `/go/{offer_id}` grava `offer_landing_visits`. Não use GET de validação, pois criaria evento de visita.
4. POST `/out/{offer_id}` grava clique após validar oferta e URL, mas na main não há token de uso único. Não enviar POST de homologação.
5. `p0_conversion_gate.py` rejeita conversão manual, mas `verified_rows` na main aceita provenance `verified=True` e parceiro correspondente sem exigir adapter autenticado.

## Double Check — candidatas isoladas
- PR #137 (head `d49bb705c8500acf4620482f209acc5a6ece4328`): **4/4 workflows success**, consultados diretamente. Inclui filtro de clique positivo/recente, guard prefetch, token outbound curto vinculado à oferta e de uso único, startup fail-closed e health separado de persistência.
- PR #140 (head `05306f2efe9af0d4fb7d147294a5bcce4c574b09`): **4/4 success**. Conversões bloqueadas até adapter autenticado; caller `verified=True` e hash correspondente não são prova de origem.
- PR #141 (head `3187aea0ac32bfb4ce539c4154ddbc9e70dcbb2e`): **4/4 success**. Cards usam `/go/` protegido, endpoint legado é redirect de compatibilidade.
- Wero1all PR #47 (head `e4d47ecdf101b3184db8d8660b02bb2de107873c`): **2/2 success**. TAG1 e TAG2 precisam ser positivas independentemente; sinais continuam caller-supplied, não autenticados.
Todas as candidatas permanecem Draft, sem merge. CI positivo não substitui homologação HTTP, backup/restore, isolamento e rollback.

## 🔴 P0 — staging Render
- Wero1Mercados staging: `srv-db6k648473hc73dkvk70`, branch antiga `dev/p0-provider-reconciliation-20261012`, auto-deploy desligado, health path vazio, Oregon.
- Wero1Divulgação staging: `srv-db79kdm7bikc73a1rv20`, branch `feat/wero1divulgacao-bootstrap`, auto-deploy desligado, health path vazio, Oregon.
- Nenhum deploy de candidata nesta rodada. HTTP runtime staging não homologado; a PR #47 não está implantada.

## 🟠 P1 — Metricool
Marca NeyMareSol (ID 7259526):
- Instagram conectado: `@neymaresoloficial`; alvo desejado: `@neymaresol` — contas distintas.
- Facebook e TikTok conectados.
- Agendamentos de 28/11 a 05/12: 0.
- TikTok 21–28/11: 25 vídeos, 677 visualizações, 66 likes, 2 comentários, 0 compartilhamentos; reach não consultado nesta rodada.
- Facebook Feed Posts e Instagram Feed Posts: analytics retornaram `rows=[]` para 21–28/11. Isso não comprova que não houve publicação; apenas que nenhum registro foi retornado.
- SmartLinks timeline (visitas, cliques em botões/imagens): `rows=[]` no período; atribuição por campanha não comprovada.
- Melhor horário relativo de sábado: Facebook 10h score 8.850, TikTok 10h score 852. Para domingo: Facebook 10h score 7.653, TikTok 10h score 816. Instagram scores 0. A janela de sábado 10h já passou nesta consulta.
Scores são recomendações relativas, não previsão de vendas. Nenhum post foi criado/agendado.

## 🟠 Sinal público autorizado — conteúdo orgânico
Senacon/MJSP, cartilha publicada em 25/11/2026: comparar preço anterior e preço final (frete/taxas/juros), verificar reputação e URL oficial, confirmar destinatário Pix/boleto e evitar falsa urgência.
Fonte: https://www.gov.br/secom/pt-br/acompanhe-a-secom/noticias/2026/11/cartilha-do-ministerio-da-justica-e-seguranca-publica-orienta-consumidores-nas-compras-da-black-friday

**Proposta editorial (não publicada):** Werozinha “4 checks antes do clique”: preço histórico, preço total, domínio/vendedor, beneficiário do pagamento.

## Integridade financeira
- Vendas comprovadas: 0.
- Conversões: 0.
- Comissões: R$ 0,00.
- Pagamentos: R$ 0,00.

## Próximos gates
1. Recuperar/migrar PostgreSQL de produção.
2. Provar conexão Render → Neon e schema apropriado.
3. Backup e restore isolado.
4. Homologar health/ready sem confundir conectividade com durabilidade.
5. Validar `/go/` e `/out/` por testes isolados que não criem eventos reais.
6. Integrar adapter de parceiro autenticado e replay/uniqueness controls.
7. Double Check combinado, rollback comprovado e promoção aprovada.
8. P2 visual/escala somente depois.

**Escritas nesta rodada:** somente este relatório em branch documental isolada. Nenhuma alteração Render/Neon, merge, deploy, anúncio, gasto, publicação, clique, conversão, venda, comissão ou pagamento. Wero1Operário e Wero1Elétrico permanecem intocados.
