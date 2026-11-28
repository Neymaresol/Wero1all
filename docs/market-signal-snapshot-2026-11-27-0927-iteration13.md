# PARADIGMA — Snapshot operacional da Iteração 13
**Data de verificação:** 27/11/2026, 09:27 BRT  
**Escopo:** Wero1Mercados / Wero1Divulgação. Somente diagnósticos, CI e uma prova operacional de persistência em Neon staging. Nenhuma promoção de produção.

## Decisão
**HOLD — produção comercial não liberada.** O PostgreSQL Render solicitado não existe mais na conta; o projeto Neon denominado produção está sem tabelas; o staging tem esquema persistido, mas nenhuma oferta elegível e nenhum evento comercial.

## P0 — Render
- Serviço de produção: `wero1mercados`, `srv-db2fvq4s728c73cahjq0`, branch `main`, plano Free, auto-deploy por commit ativo.
- Health Check Path vazio; serviço não suspenso.
- Nenhuma instância PostgreSQL encontrada na conta Render.
- Consulta direta ao ID antigo `dpg-db2h93h7lnhs73ev17og-a` retornou HTTP 404.
- O ID e a data de expiração informada (05/11/2026) estão vencidos/inexistentes; não recriar nem trocar conexão sem plano de migração, backup e rollback.
- Eventos Render entre 26/11 12:00Z e 27/11 12:20Z: 10 `server_failed`, todos `nonZeroExit=3`; a segunda página ficou vazia. Não houve `server_available` no conjunto consultado.
- Métricas de CPU, memória, HTTP, latência e instâncias: séries vazias de 27/11 06:00Z a 12:20Z.
- Logs de aplicação: consulta repetida retornou lista vazia e `hasMore=false`; consulta anterior recebeu 503 temporário.
- Último deploy Live listado: 23/10/2026, commit `80018a1c3b4a41d8bb052ddf798b11b10d613afa`.
- Wero1Mercados staging: `srv-db6k648473hc73dkvk70`, branch `dev/p0-provider-reconciliation-20261012`, auto-deploy desligado, Health Check vazio, métricas sem séries.
- Wero1Divulgação staging: `srv-db79kdm7bikc73a1rv20`, branch `feat/wero1divulgacao-bootstrap`, auto-deploy desligado, Health Check vazio, métricas sem séries.

## P0 — Neon: produção versus staging
### Projeto Neon produção
- Projeto `long-tooth-35390946`, nome `wero1mercados-production`; branch `main` (`br-spring-hall-b5ed425u`) em estado Ready.
- 0 tabelas públicas; 0 snapshots; schedule de snapshots vazio.
- Quota do plano gratuito da organização renova em 01/12/2026. Isso é reset de quota, não a expiração do antigo PostgreSQL Render.
- Não há prova de que Render esteja conectado a este projeto Neon.

### Projeto Neon staging
- Projeto `floral-hat-53843763`, nome `wero1mercados-staging`; branch `main` (`br-autumn-salad-b4cg34pj`) Ready.
- 15 tabelas públicas.
- Contagens read-only: `product_offers=19`, `offers=20`, `partners=2`, `products=19`, `clicks=0`, `conversions=0`, `outbound_action_tokens=0`, `affiliate_conversion_audit=0`, `affiliate_conversion_ledger=0`, `catalog_visits=0`, `offer_landing_visits=0`.
- `product_offers`: 19 ativas; 0 disponíveis; 0 `provider_verified`; 0 com preço positivo; 0 com comissão positiva; 0 atualizadas nos últimos 7 dias; elegíveis=0.
- Consulta de `information_schema.columns`: nenhuma coluna contendo `intent`, `int_1`, `int_2`, `tag1` ou `tag2`.
- Snapshots: 0; schedule: vazio.
- Prova operacional de persistência: inserido somente um registro em `ops_persistence_probe` com ID `paradigma-auto11-20261127-0917-bst`, finalidade explicitamente não comercial; SELECT subsequente recuperou o mesmo ID, timestamp e finalidade. Total de probes: 59. Nenhum clique, conversão, venda, comissão ou pagamento foi criado.

## P0 — Código e proveniência
### `main` atual de Wero1Mercados
- HEAD lido: `1b17084ee04c910d19a694bf79dd4f6bb4ea4516`.
- Startup executa `init_db()` e seeds sem opt-in explícito.
- `/health` usa `SELECT 1` e expõe `storage_persistent=database_ok`; conectividade não comprova durabilidade.
- GET `/go/{offer_id}` grava `offer_landing_visits`.
- POST `/out/{offer_id}` registra clique sem token HMAC de uso único.
- `/api/premium/ai-ranking` usa LEFT JOIN sem HAVING: inclui ofertas ativas com zero cliques e sem atividade recente.
- A ingestão manual de conversão chama `reject_unverified_manual_conversion` e falha fechada; não existe adapter de parceiro autenticado integrado. Portanto, não há conversão comercial liberada.
- O ranking atual não calcula INT.1/INT.2; a estrutura Neon staging também não possui colunas correspondentes.

### Candidato consolidado PR #98
- Branch `fix/p0-intent-failclosed-20261023`, HEAD `8e1f13a0b8f515869d214ebb6947eee5eb88cf44`, Draft, aberta, sem merge.
- Startup DDL/seeds exige opt-in explícito.
- Health distingue conectividade de persistência e não afirma durabilidade com `SELECT 1`.
- GET `/go/` não grava evento; emite token vinculado à oferta/canal/campanha.
- POST `/out/` valida e consome token HMAC de uso único antes de registrar clique; replay é rejeitado.
- Ranking exige pelo menos um clique total e um clique nos últimos sete dias.
- INT.1/INT.2 permanece fail-closed sem pipeline independente de eventos autenticados.
- Conversão manual continua bloqueada até adapter server-side autenticado.
- Quatro workflows do HEAD concluídos com sucesso: Wero1 campaign checks, PARADIGMA P0 Double Check, P0 Commercial Contract Double Check e P0 Isolated PostgreSQL Double Check.
- PRs #135, #137, #140 e #141 também têm quatro workflows de CI concluídos com sucesso. #140 e #141 são follow-ups empilhadas sobre #137; #135 é candidata separada. Todas Draft/abertas. Não mesclar isoladamente nem promover.
- PR #98 não foi implantada; runtime Render, identidade do banco, segredo HMAC, backup restaurável e rollback ainda não homologados.

## P1 — Wero1Divulgação
- Render staging continua apontando para `feat/wero1divulgacao-bootstrap`, auto-deploy desligado.
- Código de staging `app.py` versão `0.4.0-dev`: publicação e anúncios pagos desativados; integrações não configuradas; catálogo bloqueado sem fonte autorizada; ranking bloqueado sem fonte autorizada.
- `intent.py` exige TAG1>0 e TAG2>0 independentemente. TAG1/TAG2 são sinais públicos consultivos fornecidos ao helper, não evidência autenticada INT.1/INT.2.
- O endpoint `/api/intent/rank` retorna lista vazia enquanto os sinais forem caller-supplied e não autenticados.
- A branch `main` de Wero1all não contém `wero1divulgacao/app.py`; a integração não está na produção.
- PR #47 (TAG1/TAG2 positivos) e PR #50 (status explicitamente fail-closed) continuam Draft/abertas; dois workflows de Double Check concluídos com sucesso em cada HEAD.

## P1 — Metricool
- Marca NeyMareSol, ID `7259526`, timezone `America/Sao_Paulo`.
- Instagram conectado: `@neymaresoloficial`; perfil desejado `@neymaresol` continua divergente/não conectado.
- Facebook conectado (ID de página `102552892426549`); TikTok conectado `neymaresoltiktok`.
- Posts agendados de 27/11 a 04/12: 0.
- Analytics 20–27/11: Facebook feed posts sem linhas; SmartLinks sem linhas; Instagram com 45 seguidores nos snapshots 20–25/11 e sem valores positivos de conteúdo em 27/11.
- TikTok: 14 linhas de vídeo; 350 views, 43 likes, 2 comentários e 0 compartilhamentos no período consultado.
- Atribuição por campanha não comprovada.
- Melhores horários do Metricool são scores relativos, não previsões de vendas: Facebook sexta 10h/12h/11h, sábado 10h/11h/12h; TikTok sexta 10h/12h/18h, sábado 10h/12h/18h. Nenhum post foi agendado.

## Sinal público autorizado
- Senacon/MJSP, cartilha de compras seguras publicada em 25/11/2026: comparar preço final incluindo frete/taxas/juros; verificar reputação e domínio oficial; desconfiar de descontos excessivos e urgência artificial; conferir destinatário Pix/boleto; guardar comprovantes.
- Procon-SP publicou em 25/11/2026 pesquisa comportamental com 585 participantes sobre preços e promoções de Black Friday. Uso editorial somente; não é dado de catálogo nem sinal autenticado de intenção.
- Fontes: https://www.gov.br/mj/pt-br/assuntos/noticias/senacon-lanca-cartilha-com-orientacoes-para-compras-seguras-na-black-friday/ e https://www.procon.sp.gov.br/noticias/

## Integridade
Nenhum merge, deploy, alteração de produção, anúncio pago, gasto, publicação, clique, conversão, venda, comissão ou pagamento foi criado. A única escrita foi a prova operacional não comercial no Neon staging. Wero1Operário e Wero1Elétrico permaneceram intocados.

## Gates restantes
1. Recuperar/migrar o banco de produção com plano explícito, identidade confirmada e backup restaurável.
2. Provar que Render staging aponta exclusivamente para Neon staging.
3. Provisionar segredo HMAC por canal seguro, sem expô-lo em chat.
4. Homologar health/readiness e os fluxos `/go/` e `/out/` no staging isolado, com teste de replay e rollback.
5. Integrar adapter de parceiro com assinatura/credencial, identidade do parceiro, deduplicação e replay protection.
6. Reconciliar PRs sobrepostas em uma única cadeia, reexecutar Double Check integrado e só então avaliar promoção.
