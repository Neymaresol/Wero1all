# PARADIGMA Wero1Mercados/Wero1Divulgação — Iteração 32

**Data/hora:** 28/11/2026, 04:11 BRT  
**Escopo:** inspeção read-only de produção/staging, SQL read-only, revisão de PRs/CI, Metricool e sinais públicos.  
**Decisão:** HOLD — produção não liberada.

## P0 — Render produção

- Serviço Wero1Mercados: `srv-db2fvq4s728c73cahjq0`; branch `main`; plano Free; auto-deploy ligado; 1 instância configurada; serviço não suspenso; Health Check Path vazio.
- PostgreSQL Render `dpg-db2h93h7lnhs73ev17og-a`: API retorna 404/not found. Inventário Render não lista instância Postgres.
- Expiração informada do banco gratuito: 05/11/2026, já ultrapassada.
- Eventos: primeira página retornou 25 `server_failed`, exit code 3; 5 eventos dentro das últimas 24 horas. Último evento: 2026-11-27 18:54:24 UTC (15:54:24 BRT).
- Logs confirmam `psycopg.OperationalError` com falha DNS ao resolver hostname antigo, seguida de `Application startup failed. Exiting.`
- CPU, memória, instâncias, requisições HTTP e latência: sem séries nas últimas 24h.

## P0 — Neon e catálogo (read-only)

**Produção:** projeto `long-tooth-35390946`, branch `br-spring-hall-b5ed425u` (main), Ready; 0 tabelas públicas e 0 snapshots.  
**Staging:** projeto `floral-hat-53843763`, branch `br-autumn-salad-b4cg34pj` (main), Ready; 15 tabelas públicas.

Contagens staging:
- `product_offers`: 19 total/19 ativas; 0 disponíveis; 0 verificadas pelo provedor; 0 com preço positivo; 0 com comissão positiva; 0 atualizadas em 7 dias.
- `offers`: 20 total/19 ativas; `partners`: 2 total/1 ativo.
- Cliques 0; conversões confirmadas 0; outbound tokens 0; auditoria de conversão 0; ledger 0; visitas de catálogo 0; visitas landing 0.
- Probes operacionais: 61. Readback do último probe: `paradigma-auto11-20261128-0011-bst`, `checked_at=2026-11-28T03:13:44.558Z` (00:13:44 BRT); propósito explícito de verificação operacional de staging, sem evento comercial.
- Snapshots e backup/restauração demonstrados: 0/não comprovados em ambos os projetos.

## P0 — Revisão de código e CI

PRs atuais permanecem abertas/Draft; nenhum merge:
- Wero1Mercados #137 (HEAD `d49bb705c8500acf4620482f209acc5a6ece4328): startup bootstrap só com opt-in explícito de staging; health separa conectividade de persistência; /ready; ranking exige clique positivo e recente; /go/ ignora prefetch declarado; /out/ token de uso único e oferta-vinculado; INT qualificado permanece vazio.
- #140 (HEAD `05306f2efe9af0d4fb7d147294a5bcce4c574b09`): conversões continuam fail-closed até adapter server-side autenticado.
- #141 (HEAD `3187aea0ac32bfb4ce539c4154ddbc9e70dcbb2e`): cards Werozinha usam /go/.
- Wero1Divulgação #47 (HEAD `e4d47ecdf101b3184db8d8660b02bb2de107873c`): TAG1 e TAG2 precisam ser positivas separadamente.
- #50 (HEAD `b8203686def6e9036a19425f7dec135b0d0cb6f5`): status do ranking registrado como `registered_fail_closed`.

Workflow runs consultados e concluídos com sucesso:
- PR #137: 4/4 (offline tests, campaigns, PostgreSQL 17/18, commercial contract).
- PR #140: 4/4.
- PR #141: 4/4.
- PR #47: 2/2.
- PR #50: 2/2.

A API de commit-status retornou lista vazia; a verificação positiva foi baseada nos workflow runs e jobs específicos, não em commit statuses. Nenhum teste foi disparado nesta iteração.

## Runtime staging — bloqueio

- Wero1Mercados staging: branch `dev/p0-provider-reconciliation-20261012`, auto-deploy off, Health Check Path vazio, logs/eventos consultados sem registros.
- Wero1Divulgação staging: branch `feat/wero1divulgacao-bootstrap`, auto-deploy off, Health Check Path vazio, logs/eventos consultados sem registros.
- HTTP /health e /ready nos serviços Render staging não puderam ser acessados pelo navegador disponível. /go/ e /out/ não foram homologados por HTTP nesta execução; /out/ exige POST/token e não foi enviado.
- Não há prova do isolamento Render staging → Neon staging.

## P1 — Metricool

Marca `NeyMareSol` (ID 7259526), timezone America/Sao_Paulo:
- Instagram conectado: `@neymaresoloficial`; alvo desejado: `@neymaresol` (contas distintas).
- Facebook page ID 102552892426549; TikTok `@neymaresoltiktok`.
- Agendamentos de 28/11 a 05/12: 0.
- TikTok posts (21–28/11): 25; 677 views; 66 likes; 2 comentários; 0 shares; reach indisponível.
- Metricool `IGEV01` retorna 45 seguidores em seis registros diários (21–26/11) para o Instagram conectado; nenhum feed post foi retornado no período.
- Facebook posts, Instagram feed posts e SmartLinks timeline: sem linhas de analytics.
- Instagram best-time scores: todos zero.
- Melhores horários relativos no período 28/11–04/12:
  - Facebook: sábado 10h (8.850), domingo 10h (7.653), segunda 10h (15.247), terça 10h (14.999), quarta 12h (15.834), quinta 10h (12.351), sexta 10h (12.767).
  - TikTok: sábado 10h (852), domingo 10h (816), segunda 18h (1.096), terça 10h (1.136), quarta 10h (1.432), quinta 10h (1.471), sexta 10h (1.379).
  - Scores são relativos, não previsões. Nenhum post criado/agendado; atribuição por campanha não comprovada.

## Sinais públicos — candidatos editoriais (não são INT nem ofertas)

- Senacon/MJSP, 25/11: comparar preço final, frete, taxas/juros, reputação, endereço oficial e destinatário de Pix/boleto; evitar falsa urgência; direito de arrependimento em compras online. Fonte: https://www.gov.br/mj/pt-br/assuntos/noticias/senacon-lanca-cartilha-com-orientacoes-para-compras-seguras-na-black-friday
- Procon Fortaleza, 26/11: 56 produtos, 9 lojas, 2.332 registros; maior variação reportada 1.245,13%. Fonte: https://www.fortaleza.ce.gov.br/noticias/procon-fortaleza-publica-relatorio-de-variacao-de-precos-na-black-friday
- Agência Brasil/Procon-SP, 26/11: pesquisa com 585 consumidores paulistas; 69,85% disseram já ter se sentido enganados na Black Friday. Resultado de pesquisa amostral, não generalização para toda a população. Fonte: https://agenciabrasil.ebc.com.br/economia/noticia/2026-11/quase-70-dos-consumidores-ja-se-sentiram-enganados-na-black-friday

Ideia editorial orgânica: vídeo curto “4 checagens antes de clicar” (histórico de preço, preço total/frete, reputação/URL da loja e destinatário do pagamento). Proposta apenas; não publicada.

## Integridade financeira

Cliques, conversões, vendas, comissões e pagamentos comprovados: 0. Estimativas não foram contabilizadas como receita.

## Operações nesta iteração

- Nenhuma escrita comercial em Neon.
- Nenhuma alteração em Render, deploy ou merge.
- Nenhuma publicação, anúncio, gasto, clique ou venda sintética.
- Wero1Operário e Wero1Elétrico intocados.
- Próximos gates: recuperar/migrar DB de produção; backup e restore isolado; provar isolamento staging; homologar /health, /ready, /go/, /out/ por HTTP; adapter autenticado; Double Check e rollback.

**Status final: HOLD.**