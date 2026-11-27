# PARADIGMA — Snapshot operacional Wero1Mercados/Wero1Divulgação (27/11/2026, 02:15 BRT)

**Escopo:** read-only diagnóstico e documentação em branch isolada. Nenhum deploy, merge, anúncio, publicação, clique, conversão, venda ou pagamento foi criado.

## P0 — Render produção Wero1Mercados

- Serviço `srv-db2fvq4s728c73cahjq0`, branch `main`, plano Free, auto-deploy ligado, 1 instância, não suspenso.
- Health Check Path vazio.
- PostgreSQL Render: nenhuma instância listada. ID solicitado `dpg-db2h93h7lnhs73ev17og-a` não encontrado na listagem.
- Janela UTC de 24h: 10 eventos `server_failed`, todos com `nonZeroExit=3`.
- Eventos mais recentes: 27/11 às 04:19, 04:14, 04:11, 04:09 e 04:08 UTC.
- Logs de 04:19 UTC mostram falha de resolução DNS do hostname PostgreSQL, durante startup `init_db()`, seguida de `Application startup failed. Exiting.`
- Métricas Render (CPU, memória, instâncias, HTTP e latência) sem séries na janela consultada.

## P0 — Main de produção versus candidato PR #98

A main implantada é o commit `80018a1c3b4a41d8bb052ddf798b11b10d613afa`. Leitura do código atual confirmou:
- Startup chama `init_db()` e seeds automaticamente.
- O ranking premium não filtra cliques zero nem cliques recentes.
- A rota GET legada `/campanha/werozinha/amazon/{offer_id}` grava clique e redireciona, portanto não é segura para pré-fetch.
- As rotas seguras `/go/` e `/out/` não estão presentes na main; existem no candidato PR #98.
- Conversão manual é fail-closed: o endpoint invoca `p0_conversion_gate` e rejeita proveniência não verificada.

[PR #98](https://github.com/Neymaresol/wero1mercados/pull/98): Draft, aberta, sem merge. HEAD `8e1f13a0b8f515869d214ebb6947eee5eb88cf44`. Quatro workflows para esse HEAD: **4/4 success**. O candidato contém GET landing sem escrita, token HMAC de curta duração e vinculado à oferta/campanha, POST outbound com consumo único, replay 409, filtro de ranking e gate INT fail-closed. CI/PostgreSQL é isolado e não prova runtime Render.

[PR #95](https://github.com/Neymaresol/wero1mercados/pull/95) permanece Draft; não mesclar isoladamente: patch de ranking contém helper que aceita mapping de caller com `source_authenticated=True`, não autenticação independente.

## P0 — Neon, produção versus staging

**Produção** (`wero1mercados-production`, projeto `long-tooth-35390946`):
- Branch main Ready.
- 0 tabelas/views públicas.
- `written_data_bytes=0`, snapshots=0, agendamento de snapshot vazio.
- Quota free: renovação prevista em 01/12/2026.

**Staging** (`wero1mercados-staging`, projeto `floral-hat-53843763`):
- Branch main Ready; 15 tabelas públicas.
- `ops_persistence_probe=58` (readback nesta rodada; não inseri novo probe).
- `product_offers=19`; `offers=20`; `partners=2`.
- Cliques=0; conversões=0; landing visits=0; catalog visits=0; outbound tokens=0; conversion audit=0; commission ledger=0.
- Snapshots=0; agendamento de snapshot vazio; quota free renova 01/12/2026.

Persistência de staging é confirmada pelos registros existentes e readback SQL. Não há backup restaurável comprovado, nem vínculo Render↔Neon staging verificado.

## Render staging

- Wero1Mercados staging: branch `dev/p0-provider-reconciliation-20261012`, auto-deploy desligado, Health Check vazio, nenhum evento/log/métrica na janela consultada.
- Wero1Divulgação staging: branch `feat/wero1divulgacao-bootstrap`, auto-deploy desligado, Health Check vazio. Deploy de 25/11 05:24 UTC succeeded; nenhum log/métrica na janela consultada.
- Wero1all produção (monorepo): main, auto-deploy ligado, Health Check vazio; 0 eventos na janela consultada. Ausência de eventos não comprova health.

## P1 — Metricool (brandId 7259526)

- Instagram conectado: `@neymaresoloficial`; perfil desejado `@neymaresol` é diferente.
- Facebook e TikTok conectados.
- Agendamentos de 27/11 até 04/12: 0.
- Analytics de posts Facebook e Instagram: linhas vazias.
- TikTok, 20–27/11: 14 posts (dados concentrados em 21/11), 350 views, 43 likes, 2 comentários, 0 compartilhamentos; alcance indisponível.
- SmartLinks: sem linhas de visitas/cliques no período consultado.

### Horários recomendados pelo Metricool (não garantias)

| Dia | Facebook — top 3 | TikTok — top 3 |
|---|---|---|
| Sex. 27/11 | 10h (12.767), 12h (12.237), 11h (11.682) | 10h (1.379), 12h (1.251), 18h (1.222) |
| Sáb. 28/11 | 10h (8.850), 11h (7.880), 12h (7.871) | 10h (852), 12h (815), 18h (709) |
| Dom. 29/11 | 10h (7.653), 12h (6.913), 18h (6.739) | 10h (816), 12h (720), 18h (677) |

Instagram best-time scores estão todos zerados. Nenhum conteúdo foi criado, publicado ou agendado.

## P1 — Wero1Divulgação PR #50

[PR #50](https://github.com/Neymaresol/Wero1all/pull/50): Draft, aberta, sem merge; HEAD `b8203686def6e9036a19425f7dec135b0d0cb6f5`. Os dois workflows mais recentes para esse HEAD estão **success**; há falha histórica em commit anterior. A status API usa `registered_fail_closed` para não confundir endpoint registrado com ranking liberado.

## Decisão e gates

**HOLD — produção não liberada.** O banco antigo expirou em 05/11/2026 (data informada) e não está listado. Não contornei a restrição nem fiz write em staging nesta rodada.

Gates: recuperar/migrar DB; backup restaurável; identidade e isolamento do DB staging; segredo HMAC via canal seguro; homologar health e `/go/`/`/out/` no runtime atualizado; adapter de conversões de parceiro autenticado; Double Check e rollback.

**Financeiro:** zero cliques, conversões, comissões e pagamentos comprovados em staging. Não há números de produção reconciliáveis.
