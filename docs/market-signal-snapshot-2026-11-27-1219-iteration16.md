# PARADIGMA — Snapshot da iteração 16
**Coleta:** 27/11/2026, 12:19 BRT  
**Escopo:** Wero1Mercados / Wero1Divulgação. Auditoria read-only de infraestrutura, banco, código, CI e Metricool; atualização documental isolada. Nenhuma promoção comercial.

## 1. Render — produção Wero1Mercados

- Serviço srv-db2fvq4s728c73cahjq0, branch main, região Oregon, plano Free, auto-deploy por commit ativo, não suspenso.
- Health Check Path vazio.
- list_postgres_instances: nenhum PostgreSQL encontrado.
- Consulta direta do recurso dpg-db2h93h7lnhs73ev17og-a: HTTP 404.
- Janela 26/11 15:00Z–27/11 15:30Z: 10 eventos server_failed, todos nonZeroExit=3; página seguinte vazia.
- Log de 27/11 00:48:35Z: falha ao resolver o host dpg-db2h93h7lnhs73ev17og-a, seguida de Application startup failed.
- Métricas de CPU, memória, instâncias, HTTP e latência: séries vazias entre 06:00Z e 15:30Z.
- Deploy Live mais recente consultado: commit 80018a1c3b4a41d8bb052ddf798b11b10d613afa, criado em 21/10 e implantado em 23/10.
- O arquivo main.py da branch main chama init_db(), seed_amazon_campaigns() e seed_additional_amazon_campaigns() no startup. O endpoint /health usa SELECT 1 e copia o resultado para storage_persistent; isso não prova durabilidade.
- GET /go/{offer_id} grava offer_landing_visits; POST /out/{offer_id} grava clicks e redireciona. Não foram executados em runtime, pois a main tem efeitos comerciais nessas rotas.
- O banco Render antigo tinha expiração informada em 05/11/2026; a data já passou.

## 2. Render — staging

### Wero1Mercados staging
- Serviço srv-db6k648473hc73dkvk70, branch antiga dev/p0-provider-reconciliation-20261012.
- Auto-deploy desligado, Health Check vazio, plano Free, região Oregon.
- Último deploy Live consultado: 13/10/2026, commit 9a3741d30f18d172b2cacc147427b686100694a4.
- Sem eventos, logs ou séries de métricas na janela consultada.
- A conexão efetiva desse serviço ao projeto Neon staging não foi comprovada.

### Wero1Divulgação staging
- Serviço srv-db79kdm7bikc73a1rv20, branch feat/wero1divulgacao-bootstrap.
- Auto-deploy desligado, Health Check vazio, plano Free, região Oregon.
- Último deploy Live: 25/11/2026, commit e07b255cd6dd400ee418a8747ad19446723ce430.
- Sem eventos, logs ou séries de métricas na janela consultada.
- Tentativa de abrir /health e /api/status pelo navegador de pesquisa não foi acessível; runtime health permanece não comprovado.

## 3. Neon — produção e staging

Projetos na organização Free v3; ambos indicam renovação da quota em **01/12/2026 00:00 UTC**.

### Produção
- Projeto long-tooth-35390946, branch principal br-spring-hall-b5ed425u, estado Ready, região AWS us-east-2.
- SQL read-only: 0 tabelas públicas.
- Snapshots: 0; schedule automático: vazio.
- Nenhum vínculo Render→Neon comprovado.

### Staging
- Projeto floral-hat-53843763, branch principal br-autumn-salad-b4cg34pj, estado Ready, compute read-write ativo, região AWS us-east-2.
- 15 tabelas públicas.
- product_offers: 19 registros, 19 ativos, 0 disponíveis, 0 provider_verified, 0 com preço positivo, 0 com comissão positiva, 0 atualizados nos últimos 7 dias.
- Tabelas comerciais: offers=20, partners=2, products=19, categories=12.
- clicks=0, conversions=0, outbound_action_tokens=0, affiliate_conversion_audit=0, affiliate_conversion_ledger=0, ops_persistence_probe=59.
- Nenhuma coluna INT.1/INT.2 foi encontrada na busca de esquema; o único campo correspondente ao padrão consultado foi product_offers.provider_verified.
- Snapshots: 0; schedule automático: vazio.
- Não foi feito INSERT nesta iteração; os 59 probes são registros preexistentes. A persistência de staging já possui evidência de leitura SQL, mas backup/restauração não estão comprovados.

## 4. Código e PRs — Wero1Mercados

- O código de main ainda não exclui ranking com zero cliques: consulta LEFT JOIN clicks, calcula contagens e ordena, sem HAVING COUNT(c.id)>0 nem janela de recência.
- Isso é ranking consultivo por cliques, não pontuação INT.1/INT.2. Não há colunas INT.1/INT.2 no esquema staging consultado.
- PR #135 adiciona HAVING COUNT(c.id)>0 e pelo menos um clique nos últimos sete dias. Head 3b9405fb1f751f0301a2cf744cf90cf1a464bcf1; Draft/open; não promovida.
- PR #137 consolida ranking, prefetch, token outbound, startup e testes PostgreSQL 17/18. Head d49bb705c8500acf4620482f209acc5a6ece4328; quatro workflows reportados como success; Draft/open.
- PR #138 adiciona guard de identidade do banco staging, baseada na #137; head 8e3b351afc8c357ce8866789c32b3d3c7ef1ef86.
- PR #139 estende fingerprint para HMAC-SHA256 completo de 64 caracteres; head 0cd32771a37f20a68d836914e4eea252b4a8cbf5; empilhada sobre #138.
- PR #140 mantém conversões fail-closed até existir adapter autenticado; head 05306f2efe9af0d4fb7d147294a5bcce4c574b09; empilhada em base distinta da #139.
- PR #141 aponta cartões da vitrine para /go/; head 3187aea0ac32bfb4ce539c4154ddbc9e70dcbb2e; também empilhada sobre #137.
- PR #98 permanece Draft/open e documenta uma alternativa consolidada fail-closed; head 8e1f13a0b8f515869d214ebb6947eee5eb88cf44; quatro workflows associados reportados como success.
- Statuses combinados de commit não retornaram checks; os resultados acima vêm da listagem de workflow runs. CI em bancos descartáveis não comprova runtime Render nem backup restaurável.
- Não fazer merge: #138/#139 e #140/#141 ainda formam cadeias divergentes. A main tem auto-deploy ativo.

## 5. Wero1Divulgação

- Staging Live em e07b255, branch feat/wero1divulgacao-bootstrap, sem auto-deploy e sem Health Check.
- Código app.py versão 0.4.0-dev: publicação e anúncios pagos desligados; integrações não configuradas; catálogo bloqueado sem fonte autorizada; ranking INT bloqueado sem fonte server-side autorizada.
- PR #47 altera rank_offers() para exigir TAG1>0 e TAG2>0; head e4d47ecdf101b3184db8d8660b02bb2de107873c, dois workflows success.
- Os sinais da PR #47 continuam caller-supplied/consultivos; não autenticam INT.1/INT.2, oferta, conversão ou venda.
- PR #50 altera status do endpoint para registered_fail_closed; head b8203686def6e9036a19425f7dec135b0d0cb6f5, dois workflows success.

## 6. Metricool — marca NeyMareSol

- Brand ID 7259526; timezone America/Sao_Paulo.
- Instagram conectado: @neymaresoloficial; identificador desejado: @neymaresol — divergência permanece.
- Facebook ID 102552892426549; TikTok neymaresoltiktok.
- Posts agendados de 27/11 a 04/12: nenhum.
- Analytics 20–27/11: Facebook feed posts sem linhas; Instagram feed posts sem linhas; SmartLinks timeline sem linhas.
- TikTok: 14 vídeos em 21/11; 350 views, 43 likes, 2 comentários e 0 compartilhamentos. Dados orgânicos, não conversões ou vendas.
- Atribuição por campanha não comprovada.

## 7. Sinal público editorial — Procon-ES

Pesquisa publicada em 18/11/2026 e atualizada em 26/11/2026: mais de 40 produtos pesquisados; variações de preço chegaram a 230% entre estabelecimentos. Exemplos citados incluem churrasqueira elétrica Mondial CH 05 (R$ 140,76–R$ 464,61) e smartwatch Redmi Watch 5 Active (diferença de 167% à vista e 206% a prazo).
- Uso permitido nesta etapa: pauta editorial sobre histórico de preços, comparação de preço final, condições de pagamento, frete e entrega.
- Limite: pesquisa regional do Espírito Santo; não representa todo o Brasil, não prova preço de oferta afiliada específica e não alimenta ranking INT.
- Fonte: https://procon.es.gov.br/black-friday-pesquisa-do-procon-es-identifica-variacao-de-ate-230-nos-precos-de-produtos

## 8. Gates e decisão

1. Recuperar/migrar PostgreSQL de produção e comprovar health + persistência.
2. Comprovar isolamento Render staging→Neon staging e configurar fingerprint HMAC de 64 hex via canal seguro.
3. Comprovar backup e restore isolado.
4. Homologar /health, /ready, /go/ e /out/ apenas em staging isolado; não gerar tráfego comercial sintético.
5. Integrar adapter de parceiro que autentique origem, conta, assinatura/credencial, identidade do relatório, idempotência e replay.
6. Consolidar a cadeia #137→#138→#139 com as mudanças #140/#141, reexecutar Double Check e comprovar rollback.
7. Resolver a divergência de Instagram e configurar atribuição antes de publicação orgânica comercial.

**Decisão:** HOLD. Nenhum merge, deploy, publicação, anúncio pago, gasto, clique, conversão, venda, comissão ou pagamento foi criado nesta iteração. Wero1Operário e Wero1Elétrico permaneceram intocados.
