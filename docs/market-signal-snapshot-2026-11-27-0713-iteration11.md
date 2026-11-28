# PARADIGMA — Iteração 11 (27/11/2026, 07:13 BRT)

**Escopo:** reconciliação read-only de Render, Neon staging, GitHub e Metricool; revisão do código no commit Live e branches candidatos; novo snapshot documental na branch isolada da PR #51. Sem merges, deploys, writes em bancos, publicações ou eventos comerciais.

## P0 — Render produção Wero1Mercados

- Serviço `srv-db2fvq4s728c73cahjq0`, Free, branch `main`, auto-deploy ligado, Health Check Path vazio, não suspenso.
- Postgres Render: lista vazia; ID solicitado `dpg-db2h93h7lnhs73ev17og-a` retorna 404. A data de expiração informada (05/11/2026) já passou.
- Deploy Live atual listado: 23/10/2026, commit `80018a1c3b4a41d8bb052ddf798b11b10d613afa`.
- Logs 24h paginados: 407 registros; 16 DNS failures do host Postgres, 16 Application startup failed, 12 mensagens de restart e 14 stacktrace. Última falha observada: 27/11 04:19:13 UTC (01:19:13 BRT).
- Eventos: 10 `server_failed`, exit code 3, nas duas instâncias consultadas.
- Métricas CPU, memória, instâncias, HTTP e latência: sem séries.
- GET /health não acessível pela ferramenta de navegação; isso não equivale a um status HTTP observado.

## Render staging

- Wero1Mercados staging `srv-db6k648473hc73dkvk70`: branch `dev/p0-provider-reconciliation-20261012`, auto-deploy desligado, Health Check vazio; deploy Live de 13/10, commit `9a3741d`.
- Wero1Divulgação staging `srv-db79kdm7bikc73a1rv20`: branch `feat/wero1divulgacao-bootstrap`, auto-deploy desligado, Health Check vazio; deploy Live de 25/11, commit `e07b255`.
- Eventos, logs e métricas (CPU/memória/instâncias/HTTP/latência) em ambos: sem registros/séries na janela consultada de 24h.
- URLs `/health` e `/api/status` de staging não foram acessíveis via web tool; runtime HTTP permanece não confirmado.

## Neon — persistência e catálogo

**Produção** (`long-tooth-35390946`, branch `br-spring-hall-b5ed425u`): 0 tabelas públicas, snapshots=0, schedule vazio.

**Staging** (`floral-hat-53843763`, branch `br-autumn-salad-b4cg34pj`): 15 tabelas públicas, snapshots=0, schedule vazio. Read-only SQL:
- `product_offers`: 19 total/19 ativas; 0 disponíveis; 0 verificadas pelo provedor; 0 com preço ou comissão positiva; 0 atualizadas em 7 dias.
- `offers`: 20 total/19 ativas; 20 URLs e fontes presentes; 0 atualizadas em 7 dias.
- `partners`: 2 total/1 ativa.
- Cliques=0, conversões=0, tokens outbound=0, auditoria=0, ledger=0.
- `ops_persistence_probe`: 58 registros. Último por `checked_at`: `paradigma-iter11-20261127-0018-bst`, 27/11 03:20:52 UTC (00:20:52 BRT). Não inseri novo probe.

Readback SQL confirma persistência do staging; backup restaurável, restore e vínculo Render→Neon continuam não comprovados. Nenhuma oferta elegível.

## Double Check — código main/deploy versus candidatos

O `main.py` consultado no commit Live e na branch main tem blob SHA `1b17084ee04c910d19a694bf79dd4f6bb4ea4516`.

**Main/deploy:**
- `/api/tags/trends`: sem `HAVING COUNT(c.id) > 0`; pode incluir ofertas sem cliques.
- `/api/premium/ai-ranking`: não filtra clique zero nem exige recência de 7 dias. É ranking consultivo baseado em cliques, não INT.1/INT.2.
- GET `/go/{offer_id}`: registra visita a cada GET; sem token de ação ou guarda de prefetch.
- POST `/out/{offer_id}`: grava clique diretamente, sem token de uso único.
- Conversão manual é rejeitada, mas o gate de `p0_conversion_gate.py` aceita `Provenance.verified` declarada pelo chamador, confere parceiro e hash; não existe guard explícito de adapter autenticado.

**Candidatos isolados, todos Draft/open, não merged:**
- PR #135: filtro para clique positivo e recente (7 dias), CI 4/4 success.
- PR #137: stack consolidada com ranking positivo e recente, prefetch guard, token de ação HMAC/uso único e consume+click transacional, startup opt-in staging, INT qualificado permanece vazio sem eventos autenticados. CI 4/4 success (inclui PostgreSQL 17/18).
- PR #98: INT fail-closed; CI 4/4 success.
- PR #140: follow-up explícito `AUTHENTICATED_ADAPTER_AVAILABLE=False`, rejeita flags caller e hash até adapter server-side; CI 4/4 success.
- PR #141: vitrine usa `/go/`, GET legado não contabiliza; CI 4/4 success.
- PR #50 Wero1Divulgação: status explicitamente fail-closed; CI 2/2 success.
- PR #51 documental anterior: CI 1/1 success; o novo commit deste snapshot ainda precisa de CI.

PRs #140 e #141 são follow-ups empilhadas sobre #137; não mesclar separadamente. CI não substitui homologação Render, backup/restore, Double Check combinado e rollback.

## Wero1Divulgação

No commit Live de staging `e07b255`, o status declara publicação e anúncios pagos desativados, planejamento bloqueado por fonte de catálogo autorizada, ranking INT bloqueado por fonte autorizada e endpoint registrado fail-closed. Flags caller não autenticam oferta/sinal.

O arquivo `wero1divulgacao/app.py` não existe na branch main (404); Wero1Divulgação permanece somente em staging. Nenhum conteúdo publicado.

## P1 — Metricool (brand 7259526)

- Instagram conectado `@neymaresoloficial`, diferente do perfil desejado `@neymaresol`.
- Facebook e TikTok conectados.
- Posts agendados de 27/11 a 11/12: 0.
- Analytics de 27/11 (Facebook, Instagram e TikTok): valores retornados 0 para métricas consultadas.
- SmartLinks: sem linhas de analytics; atribuição por campanha não comprovada.
- Nenhum post criado, aprovado ou agendado.

## Sinal público editorial

**Procon de Blumenau — publicado 04/11/2026, atualizado há 22 dias:** orienta a comparar preço antes/durante a promoção para detectar “metade do dobro”, desconfiar de desconto exagerado e pressão para pagamento imediato, verificar site/CNPJ/reputação, link e destinatário Pix/boleto, custo de frete/prazo, direitos de arrependimento de 7 dias e guardar comprovantes. Aplicação editorial apenas; não autentica catálogo, ranking, INT, conversão ou comissão.

Fonte: https://www.blumenau.sc.gov.br/secao/noticias/135510

## Fechamento

- Produção HOLD; banco PostgreSQL ausente e startup falha.
- Staging Render sem logs, eventos, métricas ou health/runtime confirmado; branches antigas e auto-deploy off.
- Neon staging tem registros persistidos, mas 0 ofertas elegíveis; nenhum backup restaurável comprovado.
- Conversões permanecem bloqueadas por falta de adapter autenticado.
- Metricool sem agenda, sem analytics SmartLinks/atribuição; Instagram conectado é divergente.
- Nenhum pagamento, venda, comissão, clique ou conversão comprovados.
- Sem gastos, anúncios pagos, publicação, evento sintético, banco write, merge ou deploy.
- Wero1Operário e Wero1Elétrico intocados.

**Status: HOLD.** Gates: recuperar/migrar Postgres, backup e restore isolados, identidade do staging, segredo HMAC, runtime /health /ready /go/ /out/, adapter autenticado, Double Check e rollback.
