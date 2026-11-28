# PARADIGMA — Iteração 30 (2026-11-28 02:14 BRT)

## Escopo e segurança
Auditoria somente leitura de Render, Neon, GitHub e Metricool; nenhuma escrita comercial, nenhum clique/conversão/venda sintética, publicação, anúncio, gasto, merge ou deploy. Wero1Operário e Wero1Elétrico não foram alterados.

## P0 — Render produção
Workspace confirmado: My Workspace. Serviço `wero1mercados` (`srv-db2fvq4s728c73cahjq0`), branch `main`, plano Free, auto-deploy ligado, não suspenso, Health Check Path vazio.

- Inventário Render: nenhuma instância PostgreSQL.
- ID legado `dpg-db2h93h7lnhs73ev17og-a`: 404 / not found.
- Expiração informada para 2026-11-05: data já ultrapassada.
- Logs de aplicação: em 2026-11-27T18:49:11Z, startup chamou `init_db()` e falhou com `psycopg.OperationalError: failed to resolve host 'dpg-db2h93h7lnhs73ev17og-a'`; log seguinte reportou `Application startup failed. Exiting.`
- Métricas CPU, memória, instâncias, HTTP requests e latência: sem séries no intervalo consultado.
- Eventos Render e request logs de `/health`, `/ready`, `/go/*` e `/out/*`: nenhuma linha retornada.
- Teste HTTP externo não foi concluído: o ambiente de execução não resolveu `wero1mercados.onrender.com` nem os hosts staging. Isso é limitação de resolução DNS deste executor, não prova isolada de indisponibilidade pública.

**Conclusão:** health runtime e persistência de produção não comprovados; não implantar.

## P0 — Neon produção e staging
Ambos os projetos Neon responderam a SQL read-only e reportaram PostgreSQL 17.12, banco `neondb`, schema `public`.

### Produção
Projeto `long-tooth-35390946`, branch `main` (`br-spring-hall-b5ed425u`), estado Ready.
- `information_schema.tables` em `public`: 0 tabelas.
- Snapshots: 0.
- Schedule automático de snapshots: vazio.
- `quota_reset_at`: 2026-12-01T00:00:00Z; isso é reset de quota, não data de expiração do banco.

### Staging
Projeto `floral-hat-53843763`, branch `main` (`br-autumn-salad-b4cg34pj`), estado Ready.
- Tabelas públicas: 15.
- `product_offers`: 19; `offers`: 20; `partners`: 2.
- Cliques: 0; conversões: 0; tokens outbound: 0; auditoria de conversão: 0; ledger financeiro: 0; visitas ao catálogo: 0; visitas de landing: 0.
- `ops_persistence_probe`: 61 registros. Último readback: `paradigma-auto11-20261128-0011-bst`, 2026-11-28T03:13:44.558Z. Nenhum novo probe foi escrito nesta iteração.
- Snapshots: 0; schedule automático: vazio.

Persistência histórica no staging está confirmada por readback SQL; backup restaurável e restore isolado não estão comprovados.

## GitHub — main versus candidatas
### Defeitos ainda presentes em `main` (wero1mercados)
- Startup executa `init_db()` e seeds incondicionalmente.
- `/health` trata `SELECT 1` como `storage_persistent=true`.
- `/api/tags/trends` não tem `HAVING COUNT(c.id)>0` nem filtro de clique recente.
- `/go/{offer_id}` GET grava visita sem o guard de prefetch.
- `/out/{offer_id}` POST grava clique sem token de ação de uso único.
- `/api/premium/ai-ranking` inclui ofertas ativas sem exigir clique positivo e recente.

### PRs candidatas
- [wero1mercados #137](https://github.com/Neymaresol/wero1mercados/pull/137), Draft/open, HEAD `d49bb705c8500acf4620482f209acc5a6ece4328`: 4 workflows concluídos com success em 2026-11-21 (P0 Double Check, Commercial Contract, Campaign Checks, PostgreSQL 17/18). A candidata contém startup DDL opt-in apenas em staging, health que distingue reachability de persistência (`NOT_VERIFIED`), `/ready`, ranking consultivo com clique positivo e recente, gate INT fail-closed, guard de prefetch em `/go/` e token curto, vinculado à oferta e de uso único em `/out/`.
- [wero1mercados #140](https://github.com/Neymaresol/wero1mercados/pull/140), Draft/open, HEAD `05306f2efe9af0d4fb7d147294a5bcce4c574b09`: 4 workflows success em 2026-11-24. Adapter autenticado de parceiro continua ausente; `AUTHENTICATED_ADAPTER_AVAILABLE=False`.
- [wero1mercados #141](https://github.com/Neymaresol/wero1mercados/pull/141), Draft/open: Werozinha passa a usar `/go/{offer_id}`; compatibilidade legada não deve gravar clique.
- [Wero1all #47](https://github.com/Neymaresol/Wero1all/pull/47), Draft/open: exige TAG1>0 e TAG2>0 separadamente; 3 workflows success em 2026-11-14.
- [Wero1all #50](https://github.com/Neymaresol/Wero1all/pull/50), Draft/open: status explicitamente `registered_fail_closed`; 2 workflows success em 2026-11-27.

Os workflows são execuções históricas dos HEADs indicados, não homologação HTTP atual. Nenhuma candidata foi implantada.

## Render staging
- Wero1Mercados staging: branch antiga `dev/p0-provider-reconciliation-20261012`, auto-deploy off, Health Check Path vazio; eventos, logs, métricas e request logs sem linhas no intervalo.
- Wero1Divulgação staging: branch `feat/wero1divulgacao-bootstrap`, auto-deploy off, Health Check Path vazio; eventos, logs, métricas e request logs sem linhas.
- Código de Wero1Divulgação informa publicação desativada, integrações não configuradas, catálogo bloqueado sem fonte autorizada e ranking `BLOCKED_NO_AUTHORIZED_SIGNAL_SOURCE` / `registered_fail_closed`.

## Metricool — marca NeyMareSol (7259526)
- Instagram conectado: `@neymaresoloficial`; conta desejada: `@neymaresol` (divergência confirmada).
- Facebook conectado; TikTok conectado como `neymaresoltiktok`.
- Publicações agendadas entre 2026-11-28 e 2026-12-05: 0.
- Facebook feed posts no período: rows vazias; métricas de evolução indicam 0 posts e 0 interações na linha de 2026-11-28.
- Instagram feed posts e Reels: rows vazias; melhores horários retornaram zero.
- SmartLinks timeline: rows vazias.
- TikTok (21–28/11): 25 vídeos, 677 visualizações, 66 likes, 2 comentários, 0 compartilhamentos; último registro de seguidores 6.091 em 26/11 e variação -12 nesse dia; profile views 0 em 28/11.
- Melhor horário relativo de sábado: Facebook 10h (score 8.850), TikTok 10h (score 852), Instagram sem sinal positivo. Scores não são previsão de vendas.
- Nenhum post foi criado ou agendado; nenhuma campanha ou atribuição comercial comprovada.

## Sinais públicos autorizados — uso editorial
- Procon de Mogi das Cruzes: recomenda comparar preço final incluindo frete, condições de pagamento, prazo de entrega e troca; conferir se o desconto aparece no valor cobrado; acessar diretamente o site oficial; desconfiar de links recebidos por mensagens e conferir o destinatário do Pix. Fonte: https://www.mogidascruzes.sp.gov.br/noticia/procon-de-mogi-orienta-consumidor-a-comparar-precos-antes-de-comprar-na-black-friday
- Agência SP / Procon-SP, publicado em 2026-11-25: monitoramento de preços desde setembro para detectar maquiagem de preços; recomenda verificar CNPJ, endereço, URL e evitar links de ofertas sem origem verificada. Fonte: https://www.agenciasp.sp.gov.br/justica-e-cidadania/black-friday-procon-monitora-precos/

Sinais são editoriais e não autorizam ofertas, pontuação INT, conversões ou vendas.

## Integridade financeira
Vendas comprovadas: 0. Conversões comprovadas: 0. Comissões comprovadas: R$ 0,00. Pagamentos comprovados: R$ 0,00.

## Decisão
**HOLD.** Bloqueios: PostgreSQL Render legado ausente; Neon produção sem tabelas; sem snapshots/restore; homologação HTTP de staging não alcançada; adapter autenticado de parceiro inexistente; catálogo elegível zero; divergência do Instagram; sem atribuição de campanha. Próximos gates: recuperar/migrar DB, criar e testar backup/restore isolado, comprovar Render staging → Neon staging, homologar /health /ready /go /out, integrar origem autenticada, Double Check integrado e rollback comprovado antes de qualquer promoção.
