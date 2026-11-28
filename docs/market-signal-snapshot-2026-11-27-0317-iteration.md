# PARADIGMA — Snapshot operacional Wero1Mercados/Wero1Divulgação (27/11/2026, 03:17 BRT)

**Escopo:** somente leitura em Render/Neon/Metricool/GitHub; atualização documental isolada na branch da PR #51. Sem merge, deploy, anúncio, publicação, clique, conversão, venda ou pagamento.

## P0 — Render produção Wero1Mercados

- Serviço `srv-db2fvq4s728c73cahjq0`, `main`, Free, auto-deploy ligado, não suspenso.
- Health Check Path vazio; último update do serviço 23/10.
- Render lista zero PostgreSQL; ID solicitado `dpg-db2h93h7lnhs73ev17og-a` retorna 404.
- Janela de logs 24h paginada (5 páginas): 407 registros únicos; 16 linhas de DNS failure (`failed to resolve host`) e 16 `Application startup failed`; 12 mensagens de restart.
- Erro aponta para o hostname PostgreSQL antigo e startup `init_db()`. Últimas falhas visíveis ocorreram em 27/11 às 04:19 UTC (01:19 BRT).
- CPU, memória, instâncias, HTTP requests e latency sem séries de métricas.
- Não foi chamado endpoint live de health, porque a main executa DDL/seeds no startup e não há banco/identidade comprovados; não foi recriado banco, alterada env ou deploy.

## Render staging

- Wero1Mercados: `srv-db6k648473hc73dkvk70`, branch `dev/p0-provider-reconciliation-20261012`, auto-deploy desligado, Health Check vazio.
- Wero1Divulgação: `srv-db79kdm7bikc73a1rv20`, branch `feat/wero1divulgacao-bootstrap`, auto-deploy desligado, Health Check vazio.
- Logs e métricas CPU/memória/instâncias/HTTP/latência sem séries em ambos os serviços, na janela consultada de 24h.
- Nenhuma homologação HTTP foi realizada; o banco efetivamente conectado e o isolamento de staging não estão comprovados.

## Neon

**Produção** (`long-tooth-35390946`, branch `br-spring-hall-b5ed425u`):
- Branch Ready; consulta read-only confirmou 0 tabelas base públicas.
- `written_data_bytes=0`, snapshots=0, schedule vazio.
- Quota free reset informado: 01/12/2026.

**Staging** (`floral-hat-53843763`, branch `br-autumn-salad-b4cg34pj`):
- Branch Ready; 15 tabelas públicas.
- Probe operacional: 58 registros; último `paradigma-iter11-20261127-0018-bst`, `checked_at=2026-11-27T03:20:52.437Z` (00:20:52 BRT). Não foi inserido novo probe.
- Snapshots=0; schedule vazio; quota free reset informado 01/12/2026.
- Persistência staging comprovada por registros e readback; backup restaurável e vínculo Render↔Neon não comprovados.

## Catálogo e contadores staging (SQL read-only)

| Métrica | Valor |
|---|---:|
| product_offers | 19 |
| Ativas | 19 |
| Disponíveis | 0 |
| provider_verified | 0 |
| Preço positivo | 0 |
| Comissão positiva | 0 |
| Atualizadas em 7 dias | 0 |
| offers | 20 |
| offers active | 19 |
| offers com preço/comissão positiva | 0 |
| partners | 2 (1 ativo) |
| Cliques / conversões | 0 / 0 |
| Tokens outbound | 0 |
| Audit / commission ledger | 0 / 0 |
| Landing/catalog visits | 0 / 0 |
| ops_persistence_probe | 58 |

Nenhuma oferta está elegível para publicação/comercialização neste snapshot.

## GitHub — candidatos e CI (sem merge)

- **PR #98:** Draft; HEAD `8e1f13a0b8f515869d214ebb6947eee5eb88cf44`; 4 workflows success. Fail-closed para INT; token HMAC; GET /go sem clique; POST /out de uso único/replay guard; startup DDL/seeds opt-in; health sem afirmar durabilidade por SELECT 1. Não homologado em Render.
- **PR #135:** Draft; HEAD `3b9405fb1f751f0301a2cf744cf90cf1a464bcf1`; 4 workflows success. Patch de ranking adiciona `HAVING COUNT(c.id)>0` e exige pelo menos um clique nos últimos 7 dias. Testes são assertions estáticas do contrato; não são validação de runtime ou banco.
- **PR #137:** Draft consolidada; HEAD `d49bb705c8500acf4620482f209acc5a6ece4328`; 4 workflows success (incluindo PostgreSQL 17/18 isolado). Inclui guard de prefetch, /go e /out, conversões fail-closed, startup guard e semântica de health. CI usa banco descartável.
- **PR #140:** Draft; HEAD `05306f2efe9af0d4fb7d147294a5bcce4c574b09`; 4 workflows success. Gate explicitamente mantém `AUTHENTICATED_ADAPTER_AVAILABLE=False`, rejeitando flags/hash de caller até adaptador server-side autenticado existir.
- **PR #141:** Draft; HEAD `3187aea0ac32bfb4ce539c4154ddbc9e70dcbb2e`; 4 workflows success. Vitrine usa /go direto; endpoint Amazon legado redireciona sem contabilizar clique. Testes estáticos.
- **PR #50 Wero1Divulgação:** Draft; HEAD `b8203686def6e9036a19425f7dec135b0d0cb6f5`; 2 workflows success. Status de ranking explicitamente fail-closed.
- **PR #51:** branch documental; HEAD anterior `708bc1594e366f14ece04e564a6400b9c98b9135`; 1 workflow success. Este snapshot é documental, não integra sinais à API.
- PRs #135, #137, #140 e #141 são branches Draft/stacked ou paralelas; não mesclar separadamente. Nenhum candidato foi promovido.

## Metricool — brandId 7259526

- Instagram conectado `neymaresoloficial` (difere do perfil desejado `@neymaresol`).
- Facebook conectado (ID `102552892426549`); TikTok conectado `neymaresoltiktok`.
- Agendamentos de 27/11 a 11/12: 0.
- SmartLinks metrics no período 20–27/11: linhas vazias; atribuição por campanha sem dados.

**Analytics retornados:**
- Facebook (27/11): posts=0, interações=0, reach=0, impressões=0.
- Instagram: seguidores=45 nos registros diários 20–25/11; em 27/11 posts, views e interações=0, reach/followers null.
- TikTok (21/11): 14 vídeos, 350 views, 43 likes, 2 comentários, 0 compartilhamentos.
- TikTok followers: 6.103 no registro de 23/11.

Nenhum post foi criado, aprovado ou agendado.

## Sinais públicos/editoriais autorizados (Black Friday 27/11)

- Senacon/MJSP, cartilha publicada 25/11: comparar preço total (frete, taxas e juros), reputação e URL oficial; desconfiar de descontos excessivos, escassez/contadores; conferir destinatário Pix/boleto e guardar comprovantes.
- Senacon, notificação de 18/11 a plataformas/varejistas: atenção a fraude, publicidade afiliada, descontos artificiais, vendedor, entrega, cancelamento e reembolso.
- Procon-MT, 09/11: evitar links de social/mensagem suspeitos, verificar preços, vendedor e destinatário de pagamento.
- Procon Assembleia/ALMG, 13/11: alertas sobre ofertas falsas, deepfakes/IA e links de compra suspeitos.

**Aplicação editorial:** identificação clara de afiliado, preço total e vendedor somente quando verificáveis; sem falsa urgência/escassez, selo de vendedor ou “desconto real” não comprovados. Estes sinais não autenticam ofertas, INT.1/INT.2, conversões, comissões ou pagamentos; não foram integrados automaticamente ao ranking/API.

Fontes oficiais:
- Senacon/MJSP cartilha: https://www.gov.br/mj/pt-br/assuntos/noticias/senacon-lanca-cartilha-com-orientacoes-para-compras-seguras-na-black-friday
- Senacon notificações: https://www.gov.br/mj/pt-br/assuntos/noticias/senacon-notifica-plataformas-e-varejistas-para-prevenir-problemas-durante-a-black-friday/
- Procon-MT: https://www.procon.mt.gov.br/en/w/procon-mt-alerta-para-golpes-na-black-friday
- Procon Assembleia/ALMG: https://www.almg.gov.br/comunicacao/noticias/arquivos/Black-Friday-oportunidade-ou-risco/

## Double Check e limites

- Atualização documental somente; readback manual necessário após commit.
- Nenhum teste de runtime, staging HTTP, restore ou rollback executado nesta rodada.
- Sem escrita no Neon, Render, publicação Metricool, gasto, anúncio, clique, conversão, venda, comissão ou pagamento sintético.
- Wero1Operário e Wero1Elétrico intocados.

**Status: HOLD.** Recuperar/migrar PostgreSQL, comprovar backup/restauração e identidade/isolation de staging, provisionar segredo HMAC, homologar health/ready/go/out no runtime staging, integrar adaptador autenticado e validar rollback antes de qualquer promoção.


## P0 — Revisão do código efetivamente implantado (read-only)

Render aponta o deploy Live para commit `80018a1c3b4a41d8bb052ddf798b11b10d613afa`. A leitura de `main.py` na referência do deploy e na branch main retornou o mesmo blob SHA `1b17084ee04c910d19a694bf79dd4f6bb4ea4516` (SHA do arquivo, não do commit), confirmando que a revisão do código corresponde ao arquivo consultado.


- **Ranking atual:** SQL não contém `HAVING COUNT(c.id) > 0` nem gate de clique recente; ofertas sem cliques podem aparecer.
- **GET `/go/{offer_id}`:** existe, mas grava `offer_landing_visits` sem token de ação e sem proteção de prefetch.
- **POST `/out/{offer_id}`:** existe, valida oferta/link, porém grava clique diretamente; não consome token de uso único.
- **GET Amazon legado:** grava clique antes do redirect; pré-fetch pode produzir evento.
- **Startup:** executa `init_db()` e seeds automaticamente.

Essas condições são da main/deploy e não das PRs Draft. Não foi feito teste HTTP live devido à falha de startup/ausência de DB e ao risco de eventos de escrita. Os candidatos PR #137/#140/#141 contêm correções isoladas; não estão promovidos.
