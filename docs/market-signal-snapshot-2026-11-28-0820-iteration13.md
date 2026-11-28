# PARADIGMA — Iteração 13
**Wero1Mercados / Wero1Divulgação — 28/11/2026, 08:20 BRT**

## Decisão
**HOLD — produção não liberada.** Inspeção somente leitura em Render, Neon, GitHub e Metricool. A única escrita desta iteração é este relatório nesta branch documental isolada.

## P0 — Render
- Serviço de produção `srv-db2fvq4s728c73cahjq0`: `main`, Free, 1 instância configurada, auto-deploy por commit ativo, não suspenso, região Oregon, Health Check Path vazio.
- Inventário Render: nenhum PostgreSQL. O banco antigo `dpg-db2h93h7lnhs73ev17og-a` não aparece; a expiração informada em 05/11/2026 já passou.
- Último deploy Live: 23/10/2026, commit `80018a1c3b4a41d8bb052ddf798b11b10d613afa`.
- Exatamente 5 eventos `server_failed` na janela consultada de 24h; todos exit code 3, em 27/11 entre 18:44 e 18:54 UTC. A página seguinte não retornou eventos adicionais.
- Logs de aplicação da última hora: vazios. CPU, memória, instâncias, requisições HTTP e latência: sem séries.
- Staging Wero1Mercados: serviço `srv-db6k648473hc73dkvk70`, branch antiga `dev/p0-provider-reconciliation-20261012`, auto-deploy desligado, Health Check Path vazio, último deploy Live 13/10 no commit `9a3741d30f18d172b2cacc147427b686100694a4`; sem eventos/logs na janela de 24h.
- Staging Wero1Divulgação: serviço `srv-db79kdm7bikc73a1rv20`, branch `feat/wero1divulgacao-bootstrap`, auto-deploy desligado, Health Check Path vazio, último deploy Live 25/11 no commit `e07b255cd6dd400ee418a8747ad19446723ce430`; sem eventos/logs na janela de 24h.
- GETs de health tentados pelo navegador não foram acessíveis. Nenhum GET /go nem POST /out foi enviado: o staging de Mercados está em versão antiga e poderia gravar visita/clique. Homologação HTTP continua pendente.

## P0 — Neon
**Produção** — projeto `long-tooth-35390946`, branch `main` Ready, PostgreSQL 17.12:
- `SELECT current_database(), current_user, version(), now()` executado com sucesso: banco `neondb` alcançável.
- Schema público: 0 tabelas.
- Snapshots: 0; schedule automático vazio.
- A conexão SQL bem-sucedida prova conectividade do Neon, não integração Render→Neon nem persistência comercial da aplicação.

**Staging** — projeto `floral-hat-53843763`, branch `main` Ready, PostgreSQL 17:
- 15 tabelas públicas.
- Contagens SQL: `product_offers=19`, `offers=20` (19 ativas), `partners=2` (1 ativo); cliques, conversões, tokens outbound, auditoria, ledger, visitas de catálogo e visitas de landing = 0.
- `product_offers`: 19 ativas; disponíveis=0; provider_verified=0; preço positivo=0; comissão positiva=0; atualizadas nos últimos 7 dias=0.
- `ops_persistence_probe=61`. Último registro recuperado: `paradigma-auto11-20261128-0011-bst`, 03:13:44 UTC (00:13:44 BRT), propósito operacional de staging, sem evento comercial.
- Snapshots e schedule: vazios. Backup restaurável e restore isolado não comprovados.

## P0 — GitHub, ranking e proveniência
- `main` Wero1Mercados: SHA `1b17084ee04c910d19a694bf79dd4f6bb4ea4516`. O código de `/api/premium/ai-ranking` ainda faz LEFT JOIN em clicks e ordena por contagem, mas não tem HAVING para clique positivo/recente. Portanto, ofertas com zero clique ainda podem aparecer no ranking da produção.
- PR #137, HEAD `d49bb705c8500acf4620482f209acc5a6ece4328`, Draft: candidata adiciona `HAVING COUNT(c.id) > 0` e clique nos últimos 7 dias; separa fila consultiva de INT.1/INT.2. O filtro INT permanece vazio enquanto não existir pipeline de eventos autenticado.
- Double Check do HEAD #137: 4 workflows completed/success (PARADIGMA P0, Wero1 campaign, P0 Commercial Contract, PostgreSQL PG17/PG18).
- PR #140: 4/4 workflows success; mantém `AUTHENTICATED_ADAPTER_AVAILABLE = False`. Flag `verified=True` e hash correspondente não comprovam origem do parceiro; conversões continuam bloqueadas.
- PR #141: 4/4 workflows success; links da Werozinha passam pelo /go/ protegido.
- PR #138: 8 workflows success retornados em duas execuções; PR #139: 4 workflows success. Ambas Draft e empilhadas sobre #137; fingerprint HMAC completo não substitui staging HTTP/restore.
- Wero1all PR #47: 2/2 workflows success; TAG1 e TAG2 exigidas separadamente. PR #50: 2/2 success; status `registered_fail_closed`. Todas as PRs permanecem abertas e Draft; nenhum merge.
- Patch candidato #137 confirma prefetch guard, token outbound vinculado à oferta e de uso único, startup DDL/seed protegido por opt-in de staging, health sem alegar persistência durável por `SELECT 1`.
- O HEAD candidato não tem combined commit statuses retornados; os workflows PR concluídos foram consultados diretamente.

## P1 — Wero1Divulgação e sinais públicos
- O código `intent.py` do deploy Live de staging (commit `e07b255cd6dd400ee418a8747ad19446723ce430`) exige `tag1 > 0 AND tag2 > 0` independentemente. São sinais consultivos caller-supplied, não INT autenticado; publicação permanece bloqueada.
- Sinal oficial novo: Anvisa publicou em 27/11 a cartilha digital **“Tá na Internet. Tá na Anvisa?”**, com orientações para vendedores, marketplaces e criadores sobre regularização de produtos sujeitos à vigilância sanitária e limites de alegações publicitárias. Implicação: revisão regulatória/manual antes de divulgar medicamentos, suplementos, cosméticos, saneantes e dispositivos médicos.
- Senacon publicou em 25/11 a cartilha de compras seguras: comparar preço total com frete/taxas/juros, conferir domínio e reputação da loja, destinatário Pix/boleto, prazos e comprovantes.

## P1 — Metricool
- Marca NeyMareSol, ID `7259526`; Instagram conectado `@neymaresoloficial`, diferente do alvo `@neymaresol`; Facebook conectado (ID `102552892426549`); TikTok `@neymaresoltiktok`.
- Posts agendados de 28/11 a 05/12: 0.
- Analytics 21–28/11: Instagram feed posts 0 linhas; Facebook feed posts 0 linhas; SmartLinks timeline 0 linhas.
- TikTok: 25 vídeos, 677 visualizações, 66 likes, 2 comentários, 0 compartilhamentos; reach retornado como zero/nulo.
- Melhor horário sábado: Facebook 10h (score 8.850); TikTok 10h (score 852); Instagram todos os scores zero. Scores são recomendações relativas, não previsões de venda.
- Nenhuma publicação, agendamento ou campanha foi criada. Atribuição comercial por campanha não disponível.

## Integridade financeira
Vendas comprovadas: 0. Conversões: 0. Comissões: R$ 0,00. Pagamentos: R$ 0,00.

## Gates antes de qualquer promoção
1. Recuperar/migrar o banco de produção e provar integração Render→Neon.
2. Backup e restauração isolada comprovados.
3. Isolamento Render staging→Neon staging comprovado.
4. Homologação HTTP de /health, /ready, /go/ e /out/ sem gerar eventos comerciais artificiais.
5. Adapter server-side autenticado de parceiro com identidade, assinatura/credencial, unicidade e proteção contra replay.
6. Double Check integrado e rollback comprovado.
7. Somente depois considerar merge/deploy.

**Nesta iteração:** nenhuma alteração Render/Neon, nenhum deploy/merge, anúncio, gasto, publicação, clique, conversão ou venda sintética. Wero1Operário e Wero1Elétrico intocados.
