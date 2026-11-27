# PARADIGMA — Iteração 15 (27/11/2026, 11:15 BRT)

**Escopo:** auditoria somente leitura de Wero1Mercados/Wero1Divulgação. Este snapshot registra estados observados nos conectores; não representa homologação comercial, aprovação de oferta, venda ou comissão.

## P0 — Render produção

Serviço: `wero1mercados` (`srv-db2fvq4s728c73cahjq0`), workspace My Workspace.

- Branch: `main`; plano Free; auto-deploy por commit ativo; serviço não suspenso.
- Health Check Path: vazio.
- Lista de PostgreSQL do workspace: nenhuma instância.
- ID antigo `dpg-db2h93h7lnhs73ev17og-a`: ausente/sem resolução DNS; expiração informada em 05/11/2026 já passou.
- Deploy Live mais recente: 23/10/2026, commit `80018a1c3b4a41d8bb052ddf798b11b10d613afa`.
- O HEAD atual da `main` e o commit do deploy Live são o mesmo SHA `80018a1c3b4a41d8bb052ddf798b11b10d613afa`.
- Eventos de serviço em 24h: 10 `server_failed`, todos com `nonZeroExit=3`; nenhum evento de recuperação no intervalo consultado.
- Logs filtrados por `failed to resolve host`: 16 registros, consulta completa (`hasMore=false`). Mensagem: `psycopg.OperationalError: failed to resolve host 'dpg-db2h93h7lnhs73ev17og-a'`.
- Última ocorrência observada: 27/11/2026 04:19:13Z (01:19:13 BRT), seguida de `Application startup failed. Exiting.`.
- Séries de CPU, memória, instâncias, HTTP e latência: vazias nas últimas 24h.

**Conclusão:** produção não tem health comprovado nem persistência operacional. Nenhuma configuração, variável ou deploy foi alterado.

## P0 — Render staging

### Wero1Mercados staging

- Serviço `srv-db6k648473hc73dkvk70`; branch `dev/p0-provider-reconciliation-20261012`.
- Auto-deploy desligado; Health Check Path vazio.
- Último deploy Live: 13/10/2026, commit `9a3741d30f18d172b2cacc147427b686100694a4`.
- Eventos e séries de CPU, memória, instâncias, HTTP e latência: sem dados no intervalo consultado.

### Wero1Divulgação staging

- Serviço `srv-db79kdm7bikc73a1rv20`; branch `feat/wero1divulgacao-bootstrap`.
- Auto-deploy desligado; Health Check Path vazio.
- Último deploy Live: 25/11/2026, commit `e07b255cd6dd400ee418a8747ad19446723ce430`.
- Eventos e séries de CPU, memória, instâncias, HTTP e latência: sem dados no intervalo consultado.

Nenhum endpoint comercial foi acionado. Não se inferiu health runtime a partir de metadados de serviço.

## P0 — Neon: produção e staging

### Produção

- Projeto `wero1mercados-production`: `long-tooth-35390946`.
- Branch `main` (`br-spring-hall-b5ed425u`), estado Ready.
- Tabelas públicas: 0.
- Snapshots: 0; schedule de snapshots: vazio.

### Staging

- Projeto `wero1mercados-staging`: `floral-hat-53843763`.
- Branch `main` (`br-autumn-salad-b4cg34pj`), estado Ready.
- Tabelas públicas: 15.
- Consultas SQL foram somente leitura; nenhuma nova escrita/probe foi criada nesta iteração.

Contagens observadas:

| Indicador | Quantidade |
|---|---:|
| `product_offers` | 19 |
| `product_offers.active` | 19 |
| `product_offers.available` | 0 |
| `product_offers.provider_verified` | 0 |
| Atualizadas nos últimos 7 dias | 0 |
| Preço positivo | 0 |
| Comissão positiva | 0 |
| `offers` | 20 (19 ativas) |
| `partners` | 2 |
| `products` | 19 |
| Cliques | 0 |
| Conversões | 0 |
| Tokens outbound | 0 |
| Auditoria de conversões | 0 |
| Ledger de comissões | 0 |
| Probes operacionais existentes | 59 |

Snapshots e schedules: nenhum em produção ou staging. Persistência do staging tem registros históricos lidos por SQL, mas restauração de backup não foi demonstrada nesta iteração. A quota da organização Neon está prevista para renovar em 01/12/2026; essa data não é a expiração do banco Render antigo.

## P0 — GitHub: main e candidatos

HEAD da `main` em `wero1mercados`: `80018a1c3b4a41d8bb052ddf798b11b10d613afa`, igual ao commit Live do Render.

Leitura do código principal:

- Startup executa `init_db()` e seeds automaticamente.
- `/health` executa `SELECT 1` e usa o resultado para preencher `storage_persistent`; isso prova conectividade, não persistência durável.
- GET `/go/{offer_id}` insere em `offer_landing_visits`.
- POST `/out/{offer_id}` insere em `clicks` sem token de ação de uso único.
- `/api/premium/ai-ranking` usa `LEFT JOIN clicks` sem HAVING para excluir zero cliques ou exigir recência.
- Endpoint legado de conversões rejeita entrada manual sem adapter autenticado; adapter de parceiro autenticado não está integrado.
- `channel` e `campaign` são rótulos normalizados fornecidos pelo chamador, não prova de origem.

PRs P0 abertas e Draft; nenhuma foi mesclada:

| PR | Escopo | CI observado |
|---|---|---|
| #98 | Gate INT fail-closed e proteções do funil | 4/4 workflows concluídos com sucesso |
| #135 | Excluir ranking com zero cliques ou sem clique nos últimos 7 dias | 4/4 |
| #137 | Funil fail-closed consolidado | 4/4 |
| #138 | Fingerprint de banco staging | 8 execuções de workflow registradas, todas concluídas com sucesso |
| #139 | HMAC SHA-256 completo para fingerprint | 4/4 |
| #140 | Conversões fail-closed sem adapter autenticado | 4/4 |
| #141 | Cards da vitrine encaminhados a `/go/` | 4/4 |

Cadeia ainda não consolidada: #138 depende de #137; #139 depende de #138; #140 e #141 partem diretamente de #137 e não incluem a cadeia completa de identidade do banco. CI isolado não equivale a homologação runtime integrada.

Em Wero1Divulgação, PR #47 (TAG1 e TAG2 positivas independentemente) e PR #50 (status fail-closed) permanecem Draft; seus workflows observados concluíram com sucesso. PR #51 é documental, Draft, e seu workflow observado concluiu com sucesso.

## P1 — Metricool

Marca: NeyMareSol, ID `7259526`, fuso `America/Sao_Paulo`.

- Instagram conectado: `@neymaresoloficial`; perfil desejado informado: `@neymaresol` (divergência mantida).
- Facebook e TikTok conectados.
- Publicações agendadas de 27/11 a 04/12: 0.
- SmartLinks timeline: nenhuma linha; atribuição por campanha não comprovada.

Analytics retornados para 20–27/11:

- Facebook: em 27/11, 0 feed posts, 0 interações, 0 impressões e 0 conteúdos totais; o campo de seguidores retornou 2 nos snapshots de 20–25/11.
- Instagram: 45 seguidores nos snapshots de 20–26/11; em 27/11, 0 feed posts, 0 views e 0 interações/conteúdos totais.
- TikTok: em 21/11, 14 vídeos, 350 views, 43 likes, 2 comentários, 0 compartilhamentos e 45 interações; seguidores 6.103 no snapshot de 23/11.

Os dados do TikTok são snapshots históricos, não atividade atual. Nenhuma publicação foi criada, editada ou agendada.

## P1 — Sinais públicos autorizados

- Senacon publicou em 25/11/2026 cartilha de compras seguras para a Black Friday, cobrindo pesquisa de preços, reputação da loja, descontos excessivos, pagamento, frete, parcelamento, entrega, devolução e reembolso: https://www.gov.br/mj/pt-br/assuntos/noticias/senacon-lanca-cartilha-com-orientacoes-para-compras-seguras-na-black-friday
- Senacon notificou plataformas e varejistas em 18/11/2026 sobre medidas de proteção ao consumidor durante a Black Friday: https://www.gov.br/mj/pt-br/assuntos/noticias/senacon-notifica-plataformas-e-varejistas-para-prevenir-problemas-durante-a-black-friday

Aplicação editorial: só publicar preço/desconto, frete e condições que possam ser comprovados; identificar publicidade afiliada; não criar falsa urgência nem escassez. Esses sinais não são dados de catálogo, INT, conversões ou vendas.

## Integridade e decisão

- Nenhuma escrita em produção, merge, deploy, alteração de configuração, anúncio pago ou publicação.
- Nenhuma venda, comissão, clique, conversão ou pagamento sintético.
- Wero1Operário e Wero1Elétrico não foram alterados.
- P2 visual/escala permanece suspenso.

**Decisão: HOLD.** Gates pendentes: recuperar/migrar PostgreSQL de produção; estabelecer backup restaurável; comprovar isolamento Render staging ↔ Neon staging; consolidar fingerprint HMAC e adapter autenticado; homologar health, `/go/` e `/out/` em staging isolado; executar Double Check integrado e validar rollback.
