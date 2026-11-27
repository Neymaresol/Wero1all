# PARADIGMA — Snapshot operacional Iteração 21
Data: 27/11/2026 17:17 BRT (20:17 UTC)
Escopo: Wero1Mercados / Wero1Divulgação
Decisão: HOLD — sem promoção para produção.

## 1. Render — Wero1Mercados produção
- Workspace confirmado: My Workspace (tea-dao62kn40ujc73e210eg).
- Serviço: srv-db2fvq4s728c73cahjq0, branch main, Oregon, Free, auto-deploy por commit ativo, não suspenso.
- Health Check Path vazio; serviço tem uma configuração de instância, mas métricas de instância/CPU/memória/HTTP/latência vieram sem séries no intervalo consultado.
- Lista da conta: nenhum PostgreSQL Render.
- Consulta direta a dpg-db2h93h7lnhs73ev17og-a: 404 (not found).
- Último deploy Live continua no commit 80018a1c3b4a41d8bb052ddf798b11b10d613afa, deploy dep-dbdm4oivcj2c7388b7cg, iniciado 23/10 e ainda listado como Live.
- Eventos de 27/11 14:00–20:20 UTC: cinco server_failed, todos nonZeroExit=3, entre 18:44:11 e 18:54:24 UTC (15:44–15:54 BRT).
- Logs às 18:44:56 UTC mostram startup → init_db() → psycopg.OperationalError: failed to resolve host 'dpg-db2h93h7lnhs73ev17og-a' → Application startup failed.
- Métricas de CPU, memória, instâncias, HTTP e latência: arrays vazios.
- Tentativa de abrir /health no domínio de produção não foi acessível pela ferramenta HTTP; status HTTP não comprovado.
- Expiração informada do PostgreSQL gratuito: 05/11/2026, data já passada. Nenhuma alteração ou reinício realizado.

## 2. Render — staging
- Wero1Mercados staging: srv-db6k648473hc73dkvk70, branch dev/p0-provider-reconciliation-20261012, auto-deploy desligado, Health Check vazio. Último deploy Live: 13/10/2026, commit 9a3741d30f18d172b2cacc147427b686100694a4. Nenhum evento na janela de 14:00–20:20 UTC.
- Wero1Divulgação staging: srv-db79kdm7bikc73a1rv20, branch feat/wero1divulgacao-bootstrap, auto-deploy desligado, Health Check vazio. Último deploy Live: 25/11/2026, commit e07b255cd6dd400ee418a8747ad19446723ce430. Nenhum evento na janela de 14:00–20:20 UTC.
- Os endpoints HTTP /health e /ready de staging não foram acessíveis pela ferramenta HTTP. Ausência de eventos não comprova disponibilidade.
- Não foi comprovada a conexão Render staging → Neon staging.

## 3. Neon — produção e staging
- Produção: projeto long-tooth-35390946, branch br-spring-hall-b5ed425u, PostgreSQL 17, estado Ready. Existe banco neondb e endpoint read-write ativo ep-summer-truth-b5jp0nl1, mas get_database_tables retornou zero tabelas de usuário; snapshots: 0; schedule automático vazio. Portanto, compute ativo não comprova persistência comercial.
- Staging: projeto floral-hat-53843763, branch br-autumn-salad-b4cg34pj, PostgreSQL 17, Ready, endpoint read-write ativo ep-bold-block-b4t41tm1; 15 tabelas públicas, snapshots: 0, schedule automático vazio.
- Quota Free v3: reset informado para 01/12/2026 00:00 UTC (distinto da expiração do PostgreSQL antigo do Render).
- SQL read-only de staging:
  - product_offers: total 19; active 19; available 0; provider_verified 0; price positivo 0; commission positiva 0; source_updated_at nos últimos 7 dias 0; última atualização de origem 13/10/2026 14:32:05 UTC.
  - offers legadas: 20; partners: 2; products: 19.
  - clicks: 0; conversions: 0; outbound_action_tokens: 0; affiliate_conversion_audit: 0; affiliate_conversion_ledger: 0.
  - ops_persistence_probe: 59 registros; último readback em 27/11/2026 12:27:24 UTC, probe paradigma-auto11-20261127-0917-bst, finalidade operacional de staging sem evento comercial.
- Nenhuma escrita SQL nesta iteração.
- Esquema: product_offers não possui colunas INT.1/INT.2; outbound_action_tokens possui created_at e consumed_at, sem expires_at. A candidata aplica TTL de dez minutos pela condição em created_at. SHA-256 de relatório, isoladamente, não autentica o emissor/parceiro.

## 4. GitHub — main e candidatas P0
- Repositórios consultados: Neymaresol/wero1mercados e Neymaresol/Wero1all.
- Blob de main.py na main: 1b17084ee04c910d19a694bf79dd4f6bb4ea4516.
- Main ainda chama init_db() e seeds no startup; /health usa SELECT 1; GET /go/{offer_id} grava visita; POST /out/{offer_id} insere clique sem token; /api/premium/ai-ranking usa LEFT JOIN e não tem HAVING para excluir zero cliques nem exigir atividade recente.
- O schema staging não possui campos INT.1/INT.2. Assim, o defeito observado na main é inclusão de ofertas com zero cliques no ranking consultivo; INT permanece fail-closed e não deve ser inferido de cliques.
- PR #137: aberta, Draft, não mesclada; HEAD d49bb705c8500acf4620482f209acc5a6ece4328. Quatro workflows concluídos com success (PARADIGMA P0, Wero1 campaign checks, P0 Commercial Contract, P0 Isolated PostgreSQL PG17/PG18). Candidata exige pelo menos um clique total e um clique nos últimos sete dias; prefetch em /go/ não cria visita/token; /out/ consome token de uso único e rejeita replay/expiração; startup fica sem DDL/seeds por padrão; INT permanece bloqueado sem fonte autenticada.
- PR #140: aberta, Draft, não mesclada; HEAD 05306f2efe9af0d4fb7d147294a5bcce4c574b09. Quatro workflows success. AUTHENTICATED_ADAPTER_AVAILABLE = False; conversões continuam rejeitadas até existir adapter server-side autenticado.
- PR #141: aberta, Draft, não mesclada; HEAD 3187aea0ac32bfb4ce539c4154ddbc9e70dcbb2e. Quatro workflows success. Cartões da vitrine direcionados para /go/{offer_id}.
- CI usa bancos PostgreSQL descartáveis; não equivale à homologação HTTP no Render. Nenhuma PR foi mesclada.
- PR #98 e PR #135 continuam abertas e Draft. Não mesclar cadeias empilhadas separadamente.

## 5. Wero1Divulgação
- Código da branch feat/wero1divulgacao-bootstrap: 0.4.0-dev; blob de app.py: 2ac22c6f751daf4fcf49db1367d62afd0dbc79c0.
- /health no código retorna status=ok, mas runtime HTTP não foi comprovado.
- /api/status: publicação false, anúncios pagos false, catálogo bloqueado sem fonte autorizada, ranking INT bloqueado sem fonte autorizada.
- intent.py exige TAG1 e TAG2 estritamente positivas de forma independente; sinais enviados pelo chamador continuam consultivos, não autenticam INT.1/INT.2.
- Último deploy staging Live permanece no commit e07b255cd6dd400ee418a8747ad19446723ce430; nenhum deploy nesta iteração.

## 6. Metricool — NeyMareSol
- Brand ID 7259526, timezone America/Sao_Paulo.
- Instagram conectado: neymaresoloficial; identificador desejado: @neymaresol — divergência permanece.
- Facebook conectado (ID 102552892426549); TikTok conectado (neymaresoltiktok).
- Agendamentos de 27/11 a 04/12: 0.
- Analytics 20–27/11: Facebook feed posts retornou 0 linhas; Instagram feed posts retornou 0 linhas; SmartLinks timeline retornou 0 linhas.
- TikTok: 25 vídeos, 677 visualizações, 66 likes, 2 comentários e 0 compartilhamentos. Por data: 21/11 = 14 vídeos/403 views/43 likes/2 comentários; 25/11 = 2 vídeos/113 views/12 likes; 27/11 = 9 vídeos/161 views/11 likes.
- Atribuição por campanha não comprovada. Nenhuma publicação foi criada ou agendada.

## 7. Sinais públicos autorizados para pauta editorial
- Senacon/MJSP, cartilha publicada em 25/11/2026: comparar preço final incluindo frete, taxas e juros; conferir reputação e domínio oficial; evitar falsa urgência; validar destinatário de Pix/boleto e guardar comprovantes. Fonte: https://www.gov.br/mj/pt-br/assuntos/noticias/senacon-lanca-cartilha-com-orientacoes-para-compras-seguras-na-black-friday
- Procon-MT, monitoramento publicado em 20/11/2026: acompanhamento semanal de 30 produtos e cinco grandes lojas online; duas coletas realizadas (06 e 13/11), com monitoramento final previsto para 30/11; relatório cita aumentos semanais em itens específicos. Fonte: https://www5.sefaz.mt.gov.br/web/procon/w/procon-estadual-monitora-precos-de-produtos-mais-vendidos-na-black-friday
- Uso editorial apenas: não transformar esses sinais em oferta afiliada, preço atual, INT, venda ou comissão sem verificação individual e fonte autorizada.

## 8. Segurança, integridade e próximos gates
- Não foi executado GET/POST comercial em /go/ ou /out/: a main Live pode produzir efeitos de visita/clique e o staging Render não está isolado/conectado de forma comprovada. Runtime dessas rotas continua pendente.
- Nenhuma escrita em Render ou Neon; nenhum merge, deploy, publicação Metricool, anúncio pago, gasto, clique, conversão, venda, comissão ou pagamento sintético.
- Wero1Operário e Wero1Elétrico permaneceram intocados.
- Próximos gates: recuperar/migrar PostgreSQL Render produção; comprovar backup restaurável e restore isolado; provar conexão exclusiva Render staging → Neon staging; provisionar segredo HMAC por canal seguro; homologar /health, /ready, /go/ e /out/ em staging; integrar adapter autenticado de parceiro; consolidar PRs; executar Double Check integrado e comprovar rollback.
- Financeiro: nenhuma venda, comissão, conversão ou pagamento comprovado nesta iteração.

Conclusão: HOLD. A main continua com riscos P0; as correções candidatas passaram CI, mas não estão homologadas em runtime. Produção preservada, sem promoção.
