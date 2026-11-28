# PARADIGMA — Iteração 26
**Inspeção:** 27/11/2026, 22:18 BRT  
**Escopo:** Wero1Mercados / Wero1Divulgação  
**Decisão:** HOLD — sem promoção para produção.

## 1. Render — produção Wero1Mercados

Workspace confirmado: **My Workspace** (tea-dao62kn40ujc73e210eg).

Serviço wero1mercados (srv-db2fvq4s728c73cahjq0):
- Branch main, plano Free, região Oregon; auto-deploy por commit ativo.
- Health Check Path vazio; serviço não suspenso.
- Último deploy Live listado: 23/10/2026, commit 80018a1c3b4a41d8bb052ddf798b11b10d613afa.
- Inventário Render: nenhuma instância PostgreSQL.
- Consulta direta ao ID antigo dpg-db2h93h7lnhs73ev17og-a: HTTP 404.
- Cinco eventos server_failed entre 18:44:11 e 18:54:24 UTC em 27/11; todos exit code 3. Último às 15:54:24 BRT.
- Logs consultados de 27/11 22:00 UTC a 28/11 01:18 UTC: nenhum registro.
- Métricas de CPU, memória, instâncias, HTTP e latência nas últimas 24 horas: séries vazias.
- Endpoint público /health não acessível pela ferramenta de consulta; health runtime não comprovado.

A expiração gratuita informada para 05/11/2026 já passou. A ausência do banco foi confirmada pelo inventário vazio e pelo 404, não inferida somente da data.

## 2. Render — staging

**Wero1Mercados staging** (srv-db6k648473hc73dkvk70):
- Branch dev/p0-provider-reconciliation-20261012.
- Auto-deploy desligado; Health Check Path vazio.
- Nenhum evento entre 20/11 e 28/11.

**Wero1Divulgação staging** (srv-db79kdm7bikc73a1rv20):
- Branch feat/wero1divulgacao-bootstrap.
- Auto-deploy desligado; Health Check Path vazio.
- Último deploy em 25/11/2026, build e deploy concluídos com sucesso.
- Nenhum evento posterior na janela consultada.

As URLs de health de produção e staging não ficaram acessíveis na consulta HTTP. Não houve deploy, troca de branch ou alteração de configuração.

## 3. Neon — produção e staging

**Produção** — projeto long-tooth-35390946, branch br-spring-hall-b5ed425u:
- PostgreSQL 17, branch Ready.
- Schema público: 0 tabelas.
- written_data_bytes=0.
- Snapshots: 0; schedule automático: vazio.

**Staging** — projeto floral-hat-53843763, branch br-autumn-salad-b4cg34pj:
- PostgreSQL 17, branch Ready.
- 15 tabelas públicas.
- Snapshots: 0; schedule automático: vazio.
- SQL read-only confirmou:

| Indicador | Resultado |
|---|---:|
| product_offers | 19 |
| product_offers ativas | 19 |
| Disponíveis | 0 |
| Verificadas pelo provedor | 0 |
| Com preço positivo | 0 |
| Com comissão positiva | 0 |
| Atualizadas nos últimos 7 dias | 0 |
| offers | 20 |
| offers ativas | 19 |
| Cliques | 0 |
| Conversões | 0 |
| Tokens outbound | 0 |
| Auditorias de conversão | 0 |
| Ledger de conversão | 0 |
| Visitas ao catálogo | 0 |
| Probes operacionais | 60 |

A tabela outbound_action_tokens existe no staging, com created_at e consumed_at; não possui coluna expires_at, pois a candidata aplica TTL pela idade do registro. O schema consultado não contém campos INT.1/INT.2, assinatura ou proveniência; o único campo retornado com nome de verificação foi product_offers.provider_verified.

Os 60 probes são registros operacionais, não eventos comerciais. Nenhuma escrita SQL foi realizada nesta iteração.

Quota Neon: reset informado para 01/12/2026 00:00 UTC. Esse reset não recupera o PostgreSQL antigo do Render.

## 4. GitHub — main e candidatas

A leitura da main de Neymaresol/wero1mercados confirmou:
- Startup executa DDL e seeds.
- /health usa SELECT 1 e declara storage_persistent=true com base apenas em conectividade.
- GET /go/{offer_id} grava visita sem guard de prefetch.
- POST /out/{offer_id} grava clique sem token de uso único.
- /api/tags/trends usa LEFT JOIN sem filtro de clique positivo/recente.
- /api/premium/ai-ranking usa LEFT JOIN sem HAVING e pode incluir ofertas com zero cliques.

Candidatas continuam abertas, Draft e sem merge:
- [#137 — funil, health, ranking e token outbound](https://github.com/Neymaresol/wero1mercados/pull/137), HEAD d49bb705c8500acf4620482f209acc5a6ece4328.
- [#140 — proveniência de conversão fail-closed](https://github.com/Neymaresol/wero1mercados/pull/140), HEAD 05306f2efe9af0d4fb7d147294a5bcce4c574b09.
- [#141 — vitrine direcionada a /go/](https://github.com/Neymaresol/wero1mercados/pull/141), HEAD 3187aea0ac32bfb4ce539c4154ddbc9e70dcbb2e.
- [#47 — TAG1 e TAG2 independentes](https://github.com/Neymaresol/Wero1all/pull/47), HEAD e4d47ecdf101b3184db8d8660b02bb2de107873c.
- [#50 — ranking de divulgação explicitamente fail-closed](https://github.com/Neymaresol/Wero1all/pull/50), HEAD b8203686def6e9036a19425f7dec135b0d0cb6f5.

Workflow runs associados aos HEADs: PRs #137/#140/#141, quatro workflows concluídos com success cada; PRs #47/#50, dois workflows concluídos com success cada. Combined commit status não foi usado como evidência adicional.

A inspeção da candidata #137 confirma:
- Startup sem DDL/seeds por padrão; opt-in explícito somente em staging.
- Health distingue conectividade de persistência durável; backup/restore permanece NOT_VERIFIED.
- /ready separado.
- Prefetch/prerender declarado em /go/ retorna 204 sem visita/token.
- /out/ exige token de uso único, vinculado à oferta, TTL de dez minutos; consumo e clique são atômicos.
- Ranking consultivo exige clique total positivo e ao menos um clique nos últimos sete dias.
- Ranking INT.1/INT.2 retorna vazio até adapter autenticado.
- A candidata mantém cliques como sinal consultivo, nunca como INT ou venda.

Testes inspecionados incluem prefetch sem visita/token, token expirado, oferta inválida, replay, token vinculado à oferta, conversão legada rejeitada e guard de startup. A matriz de CI executa PostgreSQL 17/18 descartáveis e passou. Isso não substitui homologação HTTP em Render staging.

PR #140 mantém AUTHENTICATED_ADAPTER_AVAILABLE = False; booleano verified=True e hash de arquivo não autenticam o parceiro. Não há adapter de origem/conta/assinatura integrado.

## 5. Metricool — marca NeyMareSol (7259526)

Configuração retornada:
- Fuso: America/Sao_Paulo.
- Instagram conectado: @neymaresoloficial; diferente do alvo @neymaresol.
- Facebook conectado (ID 102552892426549).
- TikTok conectado (neymaresoltiktok).

Janela analítica 20–27/11:
- Publicações Facebook: nenhuma linha retornada.
- Publicações Instagram: nenhuma linha retornada.
- TikTok: 25 vídeos, 677 visualizações, 66 likes, 2 comentários, 0 compartilhamentos.
- SmartLinks timeline: nenhuma linha.
- Posts agendados entre 27/11 22:18 e 05/12 23:59 BRT: 0.

Melhores scores relativos para sábado 28/11:
- Facebook 10h: 8.850.
- TikTok 10h: 852.
- Instagram: todos os horários retornaram 0.

Scores são indicadores relativos do Metricool, não previsão de vendas. Nenhuma publicação foi criada/agendada. Atribuição por campanha não comprovada.

## 6. Sinais públicos autorizados — pauta editorial

- **Procon-ES**, pesquisa publicada em 18/11 e atualizada em 26/11: mais de 40 produtos analisados; variação de até 230% entre estabelecimentos. A pesquisa alerta para histórico de preços, frete e condições de pagamento. Fonte: https://procon.es.gov.br/black-friday-pesquisa-do-procon-es-identifica-variacao-de-ate-230-nos-precos-de-produtos
- **Procon Sergipe**, 26/11: monitoramento de 20 produtos em Aracaju e comércio online durante quatro semanas; diferenças de até 39,15% em ar-condicionado 12 mil BTUs no online, 111,23% em sanduicheira e 74,27% em smart TV 43 polegadas no levantamento presencial. Dados regionais e históricos, não preços atuais nacionais. Fonte: https://sejuc.se.gov.br/procon-sergipe-divulga-pesquisa-de-precos-para-a-black-friday-2026/
- **Anvisa**, 27/11: lançou o guia digital gratuito “Tá na Internet. Tá na Anvisa?”, com orientações para compra e divulgação online de medicamentos, suplementos, cosméticos, produtos de limpeza e dispositivos médicos; inclui orientações para influenciadores e marketplaces sobre alegações publicitárias e regularização. Fonte: https://www.gov.br/anvisa/pt-br/assuntos/noticias-anvisa/2026/black-friday-anvisa-lanca-cartilha-digital-para-compras-seguras-na-internet
- **Senacon/MJSP**, 25/11: cartilha recomenda comparar preço total, frete, taxas e juros; conferir reputação e domínio da loja; validar destinatário de Pix/boleto; guardar comprovantes e evitar falsa urgência. Fonte: https://www.gov.br/mj/pt-br/assuntos/noticias/senacon-lanca-cartilha-com-orientacoes-para-compras-seguras-na-black-friday

Esses sinais são exclusivamente editoriais. Não são feed de produtos, preço atual, estoque, TAG autenticada, INT.1/INT.2 ou conversão.

## 7. Integridade e decisão

- Nenhuma escrita em Render ou Neon.
- Nenhum merge, deploy, anúncio, gasto ou publicação.
- Nenhum clique, conversão, venda, comissão ou pagamento sintético.
- Wero1Operário e Wero1Elétrico intocados.
- Financeiro comprovado nesta iteração: zero vendas, conversões, comissões e pagamentos.

**Gates pendentes:** recuperar/migrar PostgreSQL de produção; backup restaurável e restore isolado; comprovar Render staging → Neon staging; homologar HTTP /health, /ready, /go/ e /out/; integrar adapter autenticado com assinatura, identidade de conta, anti-replay e idempotência; Double Check integrado e rollback comprovado.

**Decisão final: HOLD.** A candidata corrige o ranking zero e endurece o funil, com CI positivo, mas não está mesclada nem homologada em Render staging. Produção permanece sem PostgreSQL Render recuperado e sem proveniência comercial autenticada.
