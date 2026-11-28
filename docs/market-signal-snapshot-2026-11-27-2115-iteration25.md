# PARADIGMA — Iteração 25
**Data/hora da inspeção:** 27/11/2026 21:15 BRT  
**Escopo:** Wero1Mercados / Wero1Divulgação  
**Decisão:** HOLD — sem promoção de produção.

## 1. Render — produção Wero1Mercados

Workspace confirmado: **My Workspace** (tea-dao62kn40ujc73e210eg).

Serviço wero1mercados (srv-db2fvq4s728c73cahjq0):
- Branch main, plano Free, Oregon; auto-deploy por commit ativo.
- Health Check Path vazio; serviço não suspenso.
- Último deploy Live listado: 23/10/2026, commit 80018a1c3b4a41d8bb052ddf798b11b10d613afa.
- A listagem de Postgres do workspace retornou **nenhuma instância**.
- Consulta ao ID antigo dpg-db2h93h7lnhs73ev17og-a retornou 404.
- Eventos de 27/11: 15 server_failed, todos exit code 3; último às 18:54:24 UTC (15:54:24 BRT).
- Logs de 18:44–18:54 UTC mostram psycopg.OperationalError ao resolver o hostname antigo, seguido de Application startup failed.
- Logs entre 22:15 UTC e 00:15 UTC: nenhum registro.
- Métricas de CPU, memória, instâncias, HTTP e latência: séries vazias.
- Consulta externa de /health não ficou acessível; health runtime não comprovado.

A data de expiração gratuita informada para 05/11/2026 já passou. A ausência do recurso é confirmada pelo inventário atual e pelo 404, não por inferência de uma data de expiração.

## 2. Render — staging

**Wero1Mercados staging** (srv-db6k648473hc73dkvk70):
- Branch dev/p0-provider-reconciliation-20261012.
- Auto-deploy desligado; Health Check Path vazio.
- Último deploy Live: 13/10/2026, commit 9a3741d30f18d172b2cacc147427b686100694a4.
- Nenhum evento entre 20/11 e 28/11.

**Wero1Divulgação staging** (srv-db79kdm7bikc73a1rv20):
- Branch feat/wero1divulgacao-bootstrap.
- Auto-deploy desligado; Health Check Path vazio.
- Último deploy Live: 25/11/2026, commit e07b255cd6dd400ee418a8747ad19446723ce430.
- Build e deploy concluídos com sucesso em 25/11; nenhum evento posterior na janela consultada.
- A leitura de código confirma publicação e anúncios pagos desativados, integrações não configuradas, catálogo bloqueado sem fonte autorizada e ranking INT bloqueado.

Não foi feita troca de branch nem deploy em staging: o vínculo de ambiente e backup restaurável ainda não estão comprovados.

## 3. Neon — produção e staging

**Produção** — projeto long-tooth-35390946, branch br-spring-hall-b5ed425u:
- Branch Ready, PostgreSQL 17.
- Schema público sem tabelas base; SQL read-only retornou 0.
- written_data_bytes=0.
- Snapshots: 0; schedule automático: vazio.

**Staging** — projeto floral-hat-53843763, branch br-autumn-salad-b4cg34pj:
- Branch Ready, PostgreSQL 17; 15 tabelas públicas.
- Snapshots: 0; schedule automático: vazio.
- SQL read-only confirmou:

| Indicador | Resultado |
|---|---:|
| product_offers | 19 |
| offers | 20 |
| partners | 2 |
| Ofertas disponíveis | 0 |
| Ofertas verificadas pelo provedor | 0 |
| Ofertas com preço positivo | 0 |
| Ofertas com comissão positiva | 0 |
| Atualizadas nos últimos 7 dias | 0 |
| Cliques | 0 |
| Conversões | 0 |
| Tokens outbound | 0 |
| Auditorias de conversão | 0 |
| Ledger de conversão | 0 |
| Visitas ao catálogo | 0 |
| Probes operacionais | 60 |

O SQL consultou affiliate_conversion_audit e affiliate_conversion_ledger. Nenhuma escrita foi executada nesta iteração. O histórico de 60 probes é operacional, não comercial; não foi criado probe novo.

Quota Neon: reset informado em 2026-12-01T00:00:00Z. Isso não recupera nem substitui o banco antigo do Render.

## 4. GitHub — código e Double Check

A branch main de Wero1Mercados ainda contém:
- Startup chama init_db() e seeds automaticamente.
- /health usa SELECT 1 e atribui storage_persistent=true com base apenas em conectividade.
- GET /go/{offer_id} grava visita sem token anti-replay.
- POST /out/{offer_id} grava clique sem token de uso único.
- Ranking consultivo usa LEFT JOIN sem HAVING, permitindo ofertas com zero cliques e sem atividade recente.

As PRs candidatas permanecem abertas e Draft, sem merge:
- [#137 — funil, health, ranking e token outbound](https://github.com/Neymaresol/wero1mercados/pull/137), HEAD d49bb705c8500acf4620482f209acc5a6ece4328.
- [#140 — gate de proveniência autenticada](https://github.com/Neymaresol/wero1mercados/pull/140), HEAD 05306f2efe9af0d4fb7d147294a5bcce4c574b09.
- [#141 — vitrine via /go/](https://github.com/Neymaresol/wero1mercados/pull/141), HEAD 3187aea0ac32bfb4ce539c4154ddbc9e70dcbb2e.

Para cada HEAD, a consulta de workflow runs retornou quatro workflows concluídos com success: PARADIGMA P0 Double Check, Wero1 campaign checks, P0 Commercial Contract Double Check e P0 Isolated PostgreSQL Double Check (PG17/PG18). A API de combined commit status retornou lista vazia; a evidência positiva aqui são os workflow runs.

A leitura do código candidato confirma:
- Startup DDL/seeds somente com opt-in explícito em staging.
- /health separa conectividade de persistência e retorna NOT_VERIFIED para backup/restore.
- /ready existe na candidata.
- GET /go/ ignora prefetch/prerender declarado, emite token curto vinculado à oferta e registra landing.
- POST /out/ exige token único, com TTL de dez minutos, e consome token + grava clique na mesma transação.
- Ranking consultivo exige clique total positivo e pelo menos um clique nos últimos sete dias.
- INT.1/INT.2 continua fail-closed; cliques não são intenção autenticada.
- PR #140 mantém AUTHENTICATED_ADAPTER_AVAILABLE = False; hash de arquivo e booleano fornecido pelo chamador não autenticam o parceiro.

Esses são testes/inspeções de código e CI; não são homologação HTTP no Render. Não foram feitos requests de clique em produção.

Wero1Divulgação:
- [PR #47](https://github.com/Neymaresol/Wero1all/pull/47) e [PR #50](https://github.com/Neymaresol/Wero1all/pull/50) continuam Draft.
- Os dois workflows de Double Check de cada PR concluíram com success.
- Código staging mantém TAG1 e TAG2 independentes, mas caller-supplied; não autentica INT.1/INT.2.
- /api/plan e /api/intent/rank permanecem bloqueados sem fonte server-side autorizada.

## 5. Metricool

Marca NeyMareSol, ID 7259526, fuso America/Sao_Paulo:
- Instagram conectado: neymaresoloficial, diferente do desejado neymaresol.
- Facebook e TikTok conectados.
- Posts agendados de 27/11 a 04/12: 0.
- SmartLinks timeline: nenhuma linha de dados.

Analytics 20–28/11:
- Facebook: 2 seguidores; total de conteúdo/interações igual a 0 na linha de 28/11; nenhum conteúdo programado.
- Instagram: 45 seguidores; total de conteúdo/interações igual a 0 na linha de 28/11; nenhum conteúdo programado.
- TikTok: 25 vídeos no período, 677 visualizações, 66 likes, 2 comentários e 0 compartilhamentos. Distribuição: 14 vídeos/403 views em 21/11; 2/113 em 25/11; 9/161 em 27/11.
- Snapshot de seguidores TikTok: 6.103 em 23/11 e 6.091 em 26/11.

Horários relativos sugeridos para sábado 28/11: Facebook 10h (score 8.850) e TikTok 10h (score 852). Instagram apresenta scores zerados. Scores não são previsão de vendas. Nenhuma publicação foi criada ou agendada; atribuição por campanha não comprovada.

## 6. Sinais públicos autorizados — uso editorial

- Senacon/MJSP, 25/11/2026: cartilha orienta comparar preço final, frete, taxas e juros; verificar reputação e domínio do vendedor; desconfiar de falsa urgência; conferir destinatário de Pix/boleto; guardar comprovantes; e conhecer o direito de arrependimento em compras online. Fonte: https://www.gov.br/mj/pt-br/assuntos/noticias/senacon-lanca-cartilha-com-orientacoes-para-compras-seguras-na-black-friday
- Procon-MT, 20/11/2026: monitoramento de 30 produtos em cinco grandes lojas virtuais e lojas físicas de Cuiabá; 262 preços online e 438 presenciais coletados nas duas primeiras rodadas; nova coleta prevista para 30/11. Exemplos históricos incluem alta de 54% no OMO 3L e 22% em geladeira Brastemp 375L na Amazon. São dados regionais e históricos, não preços atuais nacionais. Fonte: https://www5.sefaz.mt.gov.br/web/procon/w/procon-estadual-monitora-pre%C3%A7os-de-produtos-mais-vendidos-na-black-friday

Esses sinais podem orientar conteúdo educativo, mas não foram importados como ofertas, preço atual, TAG autenticada, INT.1/INT.2 ou conversão. O catálogo continua sem fonte de parceiro verificada.

## 7. Integridade e decisão

- Nenhuma escrita em Render ou Neon.
- Nenhuma publicação, agendamento, anúncio pago ou gasto.
- Nenhum clique, conversão, venda, comissão ou pagamento sintético.
- Nenhum merge ou deploy.
- Wero1Operário e Wero1Elétrico não foram alterados.
- Nenhum valor financeiro foi considerado comprovado.

**Gates pendentes:** recuperar/migrar banco de produção; backup restaurável e restore isolado; provar ligação Render staging → Neon staging; homologar HTTP /health, /ready, /go/, /out/; adapter de parceiro com assinatura/identidade/replay/idempotência; Double Check integrado; rollback comprovado.

**Decisão final: HOLD.** Candidatas de código passaram nos workflows, mas a produção continua sem PostgreSQL Render, o runtime não foi comprovado e a origem comercial ainda não está autenticada.
