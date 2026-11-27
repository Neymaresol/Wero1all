# PARADIGMA Wero1Mercados / Wero1Divulgação — Iteração 11 (27/11/2026)

## Escopo
Revisão read-only de GitHub, Render, Neon staging e Metricool. Nenhuma alteração de runtime, banco, publicação ou produção. Esta atualização documental está isolada na branch `docs/market-signal-snapshot-2026-11-24`.

## P0 — Render produção
- Serviço `wero1mercados` (`srv-db2fvq4s728c73cahjq0), Free, `main`, auto-deploy ligado, Health Check vazio, não suspenso.
- Lista de Postgres Render: nenhuma instância. O ID antigo `dpg-db2h93h7lnhs73ev17og-a` retorna 404 (consulta direta).
- Expiração informada do banco gratuito: 05/11/2026, já passada.
- Eventos no período consultado: 10 `server_failed`, exit code 3.
- Logs filtrados: 16 erros de resolução DNS do host PostgreSQL; último observado em 27/11 por volta de 04:19 BRT.
- Métricas CPU, memória, HTTP, latência e instâncias: sem séries.
- Consulta de histórico de deploy Render não retornou registros; SHA/data do deploy não revalidado nesta execução.
- Último commit listado na branch GitHub main: `80018a1c3b4a41d8bb052ddf798b11b10d613afa`, datado de 21/10/2026.

## P0 — Código main (GitHub) revisado
- GET `/go/{offer_id}` grava `offer_landing_visits` em toda chamada; não usa token de ação nem guarda de prefetch.
- POST `/out/{offer_id}` registra clique sem token de ação de uso único.
- GET Amazon legado `/campanha/werozinha/amazon/{offer_id}` grava clique antes do redirect.
- Ranking `/api/premium/ai-ranking` usa LEFT JOIN de clicks, sem HAVING para excluir ofertas com zero cliques.
- Endpoint manual de conversões chama `reject_unverified_manual_conversion()` e permanece fail-closed.
- `p0_conversion_gate.py` main exige flag Provenance.verified e partner correspondente, mas `verified_rows` não contém o guard explícito de adapter autenticado presente no follow-up PR #140; proveniência caller-asserted não deve desbloquear integração.
- Startup atual executa DDL/seeds; candidate #137 adiciona opt-in explícito para staging.

## GitHub — candidatos isolados
- PR #137: Draft/open, base main; 4/4 workflows success. Inclui ranking sem clique zero, recência 7 dias, prefetch guard, token HMAC de ação e POST /out de uso único, startup opt-in e readiness conservadora.
- PR #140: Draft/open, empilhada sobre #137; 4/4 workflows success. Bloqueia `verified_rows` até existir adapter autenticado.
- PR #141: Draft/open, empilhada sobre #137; 4/4 workflows success. Cards da vitrine passam por `/go/` e endpoint Amazon legado não contabiliza clique.
- PR #135: Draft/open, base main; 4/4 workflows success; ranking zero/antigo.
- PR #98: Draft/open, base main; 4/4 workflows success; INT.1/INT.2 fail-closed.
- Nenhum candidato foi mergeado ou implantado.
- PR #50 Wero1Divulgação permanece Draft/open (não merged); 2/2 workflows success.

## Render staging
- Wero1Mercados staging: branch `dev/p0-provider-reconciliation-20261012`, auto-deploy desligado, health check vazio, sem eventos no período.
- Wero1Divulgação staging: branch `feat/wero1divulgacao-bootstrap`, auto-deploy desligado, health check vazio, sem eventos no período.
- Histórico de deploy consultado não retornou registros.
- Runtime HTTP não testado; isolamento/identidade do banco não comprovados.

## Neon
- Produção `wero1mercados-production`: branch main Ready, 0 tabelas públicas, 0 snapshots.
- Staging `wero1mercados-staging`: branch main Ready, 15 tabelas públicas, 0 snapshots.
- Read-only SQL staging: probes 58; product_offers 19; offers 20; partners 2; products 19; categories 12.
- Cliques, conversões, tokens outbound, auditoria/ledger, visitas de catálogo/landing e premium settings/change log: 0.
- Último probe lido: `paradigma-iter11-20261127-0018-bst`, 03:20:52 UTC (00:20:52 BRT), propósito explicitamente operacional, sem evento comercial.
- Persistência staging demonstrada por SQL readback; backup restaurável e conexão Render→Neon não comprovados.

## Metricool
- Brand NeyMareSol, ID 7259526; Instagram conectado `@neymaresoloficial`, diferente do desejado `@neymaresol`; Facebook e TikTok conectados.
- Posts agendados 27/11–04/12: 0.
- Facebook em 27/11: posts, interações e impressões = 0.
- Instagram: snapshot 20–25/11 = 45 followers e 22 following; 27/11 posts e views = 0.
- TikTok (21/11): 14 vídeos, 350 views, 43 likes, 2 comentários, 0 shares; followers 6.103 (23/11); profile views 0 (27/11).
- Horários sugeridos (scores, não previsão): Facebook sexta 10h=12.767, 12h=12.237; sábado 10h=8.850. TikTok sexta 10h=1.379, 18h=1.222; sábado 10h=852, 18h=709. Instagram scores 0.
- SmartLinks/campanha: nenhuma atribuição comercial verificada nesta execução.
- Nenhum post criado, publicado ou agendado.

## Fechamento
- Produção permanece HOLD; banco PostgreSQL ausente e startup falha.
- Candidato P0 possui CI aprovado, mas não está homologado no Render staging.
- Sem vendas, comissões, pagamentos ou conversões comprovados.
- Sem gastos, anúncios pagos, eventos sintéticos, writes em banco, merges ou deploys.
- Wero1Operário e Wero1Elétrico intocados.
- Gates: recuperar/migrar banco, backup/restauração, isolamento staging, segredo HMAC, runtime health e /go/ /out/, adapter autenticado, Double Check e rollback.
