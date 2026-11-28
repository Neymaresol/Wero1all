# PARADIGMA — Iteração 29
**Data de verificação:** 28/11/2026, aproximadamente 01:20 BRT  
**Escopo:** Wero1Mercados / Wero1Divulgação  
**Decisão:** HOLD — sem promoção para produção.

## 1. Render — produção Wero1Mercados

Workspace confirmado: My Workspace. Serviço `srv-db2fvq4s728c73cahjq0`, branch `main`, plano Free, Oregon, auto-deploy ligado, não suspenso, Health Check Path vazio. Último deploy Live continua em 23/10/2026, commit `80018a1c3b4a41d8bb052ddf798b11b10d613afa`.

O inventário Render não encontrou instâncias PostgreSQL. A consulta direta ao ID antigo `dpg-db2h93h7lnhs73ev17og-a` retornou HTTP 404. A expiração informada em 05/11/2026 já passou.

Eventos na janela consultada: seis `server_failed`, todos com exit code 3; o evento mais recente retornado é 28/11/2026 04:19:14 UTC (01:19:14 BRT). Logs de aplicação na última hora: vazios. Métricas CPU, memória, instâncias, HTTP e latência: sem séries. Não há health HTTP comprovado.

## 2. Neon — produção e staging separados

### Produção
Projeto `wero1mercados-production`, ID `long-tooth-35390946`, PostgreSQL 17, AWS us-east-2. Branch `main` Ready; banco `neondb`.

Consulta SQL somente leitura em 28/11/2026 04:19:18 UTC confirmou conexão com o banco e retornou **0 tabelas públicas base**. Portanto, existe um projeto Neon de produção, mas o schema público esperado pela aplicação não está presente. Não confundir este projeto Neon com o antigo PostgreSQL Render, que não foi encontrado.

Snapshots: 0. Agenda de snapshots: vazia.

### Staging
Projeto `wero1mercados-staging`, ID `floral-hat-53843763`, PostgreSQL 17, AWS us-east-2. Foram listadas 15 tabelas públicas.

Consulta SQL somente leitura:
- `product_offers`: 19 registros, 19 ativos, 0 disponíveis, 0 verificados pelo provedor.
- Ofertas com preço positivo: 0; comissão positiva: 0; atualizadas em 7 dias: 0.
- `offers`: 20 registros, 19 ativos; 19 produtos; 2 parceiros, 1 ativo.
- Cliques: 0; conversões: 0; tokens outbound: 0; auditoria: 0; ledger: 0; visitas de catálogo: 0; visitas de landing: 0.
- `ops_persistence_probe`: 61 registros. Último readback: `paradigma-auto11-20261128-0011-bst`, 28/11/2026 03:13:44 UTC (00:13:44 BRT).

Nenhum probe novo foi gravado nesta iteração. O readback histórico foi consultado novamente. Snapshots: 0; agenda: vazia. A persistência de staging não prova backup/restauração nem conexão Render→Neon.

## 3. GitHub — código atual e candidatas

Leitura direta da `main` confirmou:
- `/health` atribui `storage_persistent` ao resultado de `SELECT 1`, que comprova apenas conectividade.
- Startup chama `init_db()` e seeds sem gate explícito.
- `/api/tags/trends` não exige clique positivo/recente.
- GET `/go/{offer_id}` registra visita.
- POST `/out/{offer_id}` grava clique diretamente, sem token de uso único.

Candidatas isoladas:
- PR #137: filtro de ranking por clique e recência, gate de startup, health sem falsa garantia de persistência, readiness, guard de prefetch e token outbound. Quatro workflows concluídos com sucesso em 21/11/2026.
- PR #140: proveniência fail-closed; `AUTHENTICATED_ADAPTER_AVAILABLE = False` mantém conversões bloqueadas. Quatro workflows concluídos com sucesso em 24/11/2026.
- PR #141: links da vitrine Werozinha apontam para `/go/`; quatro workflows concluídos com sucesso em 25/11/2026.
- Wero1Divulgação PR #47: exige TAG1 e TAG2 positivas separadamente; sinais seguem `caller_supplied`, não autenticam INT.1/INT.2. Três workflows concluídos com sucesso em 14/11/2026.
- Wero1Divulgação PR #50: status `registered_fail_closed`; dois workflows concluídos com sucesso em 27/11/2026.

Todas as PRs acima permanecem abertas e Draft. Os workflows são evidência de CI nos HEADs consultados, não homologação HTTP em Render. Os combined status checks do endpoint de status retornaram lista vazia.

PR documental #51 continua Draft; atualização deste arquivo não altera código comercial.

## 4. Metricool — divulgação orgânica

Marca `NeyMareSol`, brandId `7259526`.
- Instagram conectado: `@neymaresoloficial`; diferente do alvo `@neymaresol`.
- Facebook conectado (ID `102552892426549`).
- TikTok conectado: `neymaresoltiktok`.

Analytics de 21 a 28/11:
- Facebook posts: nenhuma linha retornada.
- Instagram posts: nenhuma linha retornada.
- TikTok: 25 vídeos, 677 visualizações, 66 likes, 2 comentários e 0 compartilhamentos.

Agendamentos de 28/11 a 05/12: 0. Melhor horário relativo de sábado retornado pelo Metricool: Facebook 10h (score 8.850), TikTok 10h (score 852), Instagram sem sinal positivo (0). Scores são relativos e não previsão de venda. Nenhuma publicação foi criada ou agendada; nenhuma atribuição comercial comprovada.

## 5. Sinais públicos autorizados — uso editorial, não comercial

- Anvisa, 27/11/2026: cartilha digital “Tá na Internet. Tá na Anvisa?” orienta consumidores, vendedores, marketplaces e criadores sobre regularização e publicidade de medicamentos, suplementos, cosméticos, saneantes, dispositivos médicos e produtos relacionados ao aleitamento materno. Implicação: exigir checagem regulatória e evitar alegações terapêuticas não autorizadas.
- Senacon/MJSP, 25/11/2026: cartilha de compras seguras recomenda comparar preço total (frete, taxas e juros), verificar reputação e domínio do vendedor, conferir destinatário de Pix/boleto, revisar adicionais no carrinho e evitar falsa urgência.
- Procon-MT, 09/11/2026: alerta contra golpes na Black Friday; recomenda verificar histórico de preços, links e dados do beneficiário antes do pagamento.

Essas fontes servem para conteúdo educativo e filtros editoriais. Não são feed de ofertas, preço atual de produto, intenção INT, conversão ou prova de comissão.

## 6. Integridade e gates

Nesta iteração:
- Uma escrita documental isolada no branch de documentação do GitHub.
- Nenhuma escrita em Render ou Neon.
- Nenhum merge, deploy, anúncio pago, gasto, publicação, clique, conversão, venda, comissão ou pagamento sintético.
- Wero1Operário e Wero1Elétrico não foram alterados.

Financeiro comprovado nesta execução: vendas 0; conversões 0; comissões R$ 0,00; pagamentos R$ 0,00.

### Próximos gates obrigatórios
1. Recuperar ou migrar o PostgreSQL de produção e demonstrar o vínculo de conexão.
2. Criar backup e comprovar restauração isolada.
3. Confirmar que Render staging usa exclusivamente Neon staging.
4. Homologar por HTTP `/health`, `/ready`, `/go/` e `/out/` sem gerar eventos comerciais sintéticos.
5. Integrar adapter server-side de parceiro com autenticação, assinatura, identidade, replay protection e idempotência.
6. Double Check integrado e rollback comprovado.
7. Só então avaliar merge e promoção.

**Status final: HOLD.**
