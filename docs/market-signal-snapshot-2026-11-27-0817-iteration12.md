# PARADIGMA — Iteração 12 (27/11/2026, 08:17 BRT)

Escopo: auditoria read-only de Render, Neon, GitHub e Metricool. Única escrita nesta rodada: snapshot documental nesta branch isolada da PR #51. Sem merge, deploy, publicação, banco write, evento comercial ou alteração de produção.

## P0 — Render produção Wero1Mercados

- Serviço `srv-db2fvq4s728c73cahjq0`, branch `main`, Free, auto-deploy ligado, Health Check Path vazio, não suspenso.
- Lista de Postgres Render: vazia. ID antigo `dpg-db2h93h7lnhs73ev17og-a`: inexistente (404 na rodada anterior). A data de expiração informada (05/11/2026) passou.
- Deploy Live listado: 23/10/2026, commit `80018a1c3b4a41d8bb052ddf798b11b10d613afa`.
- Eventos últimas 24h: 10 `server_failed` retornados (página com cursor, portanto não exaustiva), todos com exit code 3.
- Logs filtrados 24h por DNS: 16 mensagens de falha na resolução do host Postgres; `hasMore=false`. Última mensagem: 27/11 04:19:13 UTC (01:19:13 BRT).
- Métricas últimas 6h: CPU, memória, instâncias, HTTP e latência sem séries.
- Health de produção não comprovado; sem teste HTTP live.

## Render staging

- Wero1Mercados staging `srv-db6k648473hc73dkvk70`: branch antiga `dev/p0-provider-reconciliation-20261012`, auto-deploy desligado, health path vazio. Eventos e métricas 24h sem dados.
- Wero1Divulgação staging `srv-db79kdm7bikc73a1rv20`: branch `feat/wero1divulgacao-bootstrap`, auto-deploy desligado, health path vazio. Eventos e métricas 24h sem dados.
- HTTP/runtime não foi testado nesta rodada; ausência de logs/métricas não comprova que esteja saudável.

## Neon — persistência

**Produção** (`long-tooth-35390946`, branch `br-spring-hall-b5ed425u`): 0 tabelas públicas, snapshots=0, schedule vazio.

**Staging** (`floral-hat-53843763`, branch `br-autumn-salad-b4cg34pj`): SQL read-only confirmou:
- `ops_persistence_probe`: 58
- `product_offers`: 19
- `offers`: 20
- `partners`: 2
- `products`: 19
- `categories`: 12
- `clicks`: 0
- `conversions`: 0
- `outbound_action_tokens`: 0
- `affiliate_conversion_audit`: 0
- `affiliate_conversion_ledger`: 0
- `offer_landing_visits`: 0
- `catalog_visits`: 0

Staging tem 15 tabelas públicas; snapshot=0 e schedule vazio. Readback SQL comprova persistência dos registros existentes, mas backup/restauração não foi comprovado. `written_data_bytes=0` é métrica de consumo/telemetria e não contradiz a leitura SQL.

## GitHub — candidatos e CI verificados

PRs seguem Draft/open, sem merge.

- #135 ranking: `HAVING COUNT(c.id) > 0` e exige pelo menos um clique nos últimos 7 dias. Patch lido. 4 workflows concluídos/success.
- #137 funil P0 consolidado: 4 workflows concluídos/success; inclui testes PostgreSQL 17/18. Candidato inclui prefetch guard, token de outbound HMAC de uso único, startup opt-in staging e readiness separada da comprovação de backup.
- #140 conversões: 4 workflows success; mantém gate fail-closed até adapter autenticado server-side. PR empilhada sobre #137.
- #141 vitrine: 4 workflows success; cards usam `/go/`, endpoint Amazon GET legado não contabiliza clique. PR empilhada sobre #137.
- #138/#139 guard de identidade de banco staging: continuam Draft, follow-ups empilhadas.
- Wero1Divulgação PR #50: 2 workflows success; status fail-closed explícito.
- PR #51 documental: 1 workflow PARADIGMA P0 Double Check success no commit anterior.

O status combinado de commits retornou lista vazia; os resultados acima vêm de runs associados aos SHAs (não de checks de status combinados). CI não substitui homologação HTTP/runtime, backup/restore, revisão integrada e rollback.

## Wero1Divulgação — staging

Código da branch `feat/wero1divulgacao-bootstrap`, SHA `2ac22c6f751daf4fcf49db1367d62afd0dbc79c0`, lido:
- `/health` declara modo staging/publication disabled (runtime HTTP não confirmado).
- `/api/status`: publicação e anúncios pagos desativados; catálogo e ranking bloqueados por fonte autorizada ausente; endpoint registrado fail-closed.
- `/api/plan` rejeita flags de oferta fornecidas pelo caller como autorização.
- `/api/intent/rank` retorna ranking vazio até adapter de sinais server-side verificar origem, data, identidade e integridade.
- `/api/simulate/happy-path` existe, mas **não foi invocado**; nenhuma venda sintética criada.
- `wero1divulgacao/app.py` não existe na branch `main` do Wero1all; integração de produção não comprovada.

## P1 — Metricool

Brand NeyMareSol, ID `7259526`, timezone `America/Sao_Paulo`.
- Instagram conectado: `@neymaresoloficial`; perfil desejado `@neymaresol` — divergência confirmada.
- Facebook/TikTok conectados.
- Posts agendados 27/11 08:00 até 04/12 23:59 BRT: 0.
- Facebook analytics (20–27/11): sem linhas retornadas.
- Instagram analytics (20–27/11): sem linhas retornadas.
- SmartLinks analytics (20–27/11): sem linhas retornadas; atribuição por campanha não comprovada.
- TikTok posts analytics retornou 14 vídeos com data 21/11: 350 views, 43 likes, 2 comentários, 0 compartilhamentos. Dados de 21/11, não representam atividade de hoje.

## Sinal editorial público

Senacon/MJSP publicou a cartilha de compras on-line Black Friday em 25/11/2026. Orientações: comparar preço total com frete, taxas e juros; verificar reputação do vendedor e URL oficial; revisar itens extras; conferir destinatário Pix/boleto; evitar contadores/escassez sem prova; guardar registros e comprovantes. Aplicação editorial, sem autenticar catálogo, INT, vendas ou comissões.

Fonte oficial: https://www.gov.br/mj/pt-br/assuntos/noticias/senacon-lanca-cartilha-com-orientacoes-para-compras-seguras-na-black-friday

## Fechamento

- Produção HOLD: Postgres Render ausente; startup DNS falha; health/persistência production não comprovados.
- Staging: SQL readback comprova persistência existente, mas catálogo elegível 0/19 e backup restaurável não comprovado.
- Ranking: correção candidata #135/#137 verificada em patch; ainda não integrada à main.
- Conversões: bloqueadas sem adapter autenticado.
- /go/ e /out/: contratos de teste CI, não live; runtime HTTP não homologado.
- Metricool: 0 posts agendados, Facebook/Instagram/SmartLinks sem dados e conta Instagram divergente.
- Nenhum pagamento, venda, comissão, clique ou conversão comprovado.
- Sem gastos, anúncios pagos, publicação, evento sintético, banco write, merge ou deploy.
- Wero1Operário e Wero1Elétrico intocados.

**Status: HOLD.** Gates: recuperação/migração Postgres, backup e restore comprovados, identidade staging, segredo HMAC, runtime /health /ready /go/ /out/, adapter autenticado, Double Check integrado e rollback.
