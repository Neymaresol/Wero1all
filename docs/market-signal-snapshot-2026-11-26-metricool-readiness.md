# PARADIGMA — Snapshot de sinais públicos e Metricool (27/11/2026)

**Revisão:** 26/11/2026, 23:27 BRT.  
**Escopo:** contexto editorial, diagnóstico de divulgação orgânica e reconciliação de staging. Documento-only; não altera runtime, catálogo, ranking, INT.1/INT.2, atribuição, vendas ou pagamentos.

## Sinais oficiais de proteção ao consumidor

- **Procon-SP (23/11/2026):** acompanha desde setembro uma amostra de produtos em grandes sites, verificando preços, condições de pagamento e possíveis sinais de “maquiagem de preços”; também informou fiscalizações presenciais e orientações para conferir URL, CNPJ, endereço e telefone. [Fonte oficial](https://www.procon.sp.gov.br/black-friday-procon-sp-monitora-precos-e-orienta-consumidores-nesta-semana/)
- **Procon-RS e Procon de Porto Alegre (26–27/11/2026):** unidade móvel de orientação no Centro Histórico de Porto Alegre, das 10h às 17h; alerta sobre falsos descontos, publicidade enganosa e golpes por links. Reforça que HTTPS/cadeado não comprova legitimidade da loja e recomenda conferir CNPJ, vendedor em marketplace, destinatário Pix e beneficiário do boleto. [Fonte oficial](https://www.procon.rs.gov.br/unidade-movel-do-procon-rs-inicia-atendimento-a-consumidores-em-parceria-com-o-procon-de-porto-alegre-durante-a-black-friday)
- **Senacon/MJSP (25/11/2026):** cartilha recomenda comparar preço final, frete, taxas e juros, conferir reputação e endereço oficial, evitar falsa urgência e guardar comprovantes. [Fonte oficial](https://www.gov.br/mj/pt-br/assuntos/noticias/senacon-lanca-cartilha-com-orientacoes-para-compras-seguras-na-black-friday)

### Uso editorial permitido

- Mensagens sobre comparar preço final, frete, prazo, vendedor, condições e histórico.
- Sem falsa urgência, contagem regressiva ou “últimas unidades” sem evidência verificável.
- Sinais públicos são contexto editorial; não autenticam parceiros, ofertas, preço, disponibilidade ou comissão.

## Metricool — consulta atualizada em 26/11/2026, 23:17 BRT

Marca NeyMareSol (brandId 7259526), timezone America/Sao_Paulo.

### Identidade e atividade

- Instagram conectado: **@neymaresoloficial**; difere do perfil desejado **@neymaresol**.
- Facebook: página conectada (ID 102552892426549).
- TikTok: conta conectada (neymaresoltiktok).
- Agendamentos consultados de 26/11 23:17 a 10/12 23:59: **0**.
- Consulta post-level do Facebook (FBPO01–FBPO14), período 20–26/11: nenhuma linha retornada.
- Consulta post-level do Instagram (IGPO01–IGPO15), período 20–26/11: nenhuma linha retornada.
- SmartLinks (SLTL01–SLTL05: visitas, cliques em botões/imagens), período 20–26/11: nenhuma linha retornada.
- Atribuição por campanha: sem dados comprovados.

### Analytics de conta (20–26/11)

- **Facebook:** campo de seguidores retornou 2,0 nos registros de 20–25/11; na linha de 26/11, seguidores vieram nulos. Para 26/11, total de conteúdo (feed posts + reels) = 0 e interações de conteúdo = 0. A consulta post-level não retornou publicações.
- **Instagram:** 45 seguidores nos registros de 20–25/11. Na linha de 26/11, feed posts = 0, views = 0, interações = 0 e total de conteúdo = 0; seguidores e alcance vieram nulos. A consulta post-level não retornou publicações.
- **TikTok:** 14 vídeos publicados em 21/11, com 350 views, 43 likes, 2 comentários e 0 compartilhamentos. O campo de seguidores retornou 6.103 em 23/11; novos seguidores retornaram 0 em 26/11.
- Valores nulos/ausentes não são zero. Métricas de redes sociais não são atribuição comercial do PARADIGMA.

### Horários sugeridos pelo Metricool para sexta-feira, 27/11

- Facebook: **10h (score 12.767)**; alternativas 12h (12.237) e 11h (11.682).
- TikTok: **10h (score 1.379)**; alternativas 12h (1.251) e 18h (1.222).
- Instagram: score 0 em todos os horários retornados.

Scores são recomendações internas do Metricool, não garantias de alcance ou engajamento. Horários são apenas sugestões; nenhuma publicação foi criada, enviada, aprovada ou agendada nesta execução.

## Catálogo — Neon staging, consulta SQL (26/11)

- Projeto: `wero1mercados-staging`; branch main Ready; 15 tabelas públicas.
- `product_offers`: 19 registros, 19 ativos.
- Disponíveis: 0; verificadas pelo provedor: 0; preço positivo: 0; comissão positiva: 0; atualizadas nos últimos 7 dias: 0.
- Elegibilidade completa: **0/19**.
- `offers`: 20; produtos: 19; parceiros: 2; parceiros ativos: 1.
- Cliques, conversões, tokens outbound, auditoria, ledger, visitas de landing e visitas de catálogo: 0 linhas.

### Persistência operacional em staging

- Probe operacional gravado e lido de volta nesta revisão: `paradigma-auto-run11-20261126-2317-bst`.
- INSERT + SELECT por ID: sucesso.
- Timestamp do banco: 2026-11-27T02:27:34.763Z (26/11, 23:27:34 BRT).
- Total após o teste: **57 probes**.
- O probe é exclusivamente operacional; não representa visita, clique, conversão, venda, comissão ou pagamento.

O readback confirma persistência no Neon staging. Não comprova backup restaurável nem conexão do Render staging ao Neon.

## Neon produção — distinção de ambiente

- Projeto `wero1mercados-production`, branch main: Ready.
- Tabelas públicas: 0.
- Snapshots: 0; agendamento de snapshots vazio.
- `written_data_bytes` no relatório de consumo: 0.
- Nenhuma evidência disponível de conexão entre esse projeto e o serviço Render de produção.

O PostgreSQL Render solicitado (`dpg-db2h93h7lnhs73ev17og-a`) não foi encontrado; consulta por ID retorna 404. Portanto, não classificar o projeto Neon separado como banco efetivo da produção Render.

## Gates e segurança

- Este snapshot não autoriza ofertas nem publica conteúdo.
- Nenhum clique, conversão, venda, comissão ou pagamento sintético foi gerado.
- Nenhuma publicação, agendamento, anúncio, gasto ou deploy de produção foi realizado.
- Nenhum merge foi realizado; esta atualização permanece em branch documental Draft.
- Wero1Operário e Wero1Elétrico permanecem intocados.
- A publicação comercial continua bloqueada até persistência/backup, identidade de banco, health, funil HTTP, catálogo elegível e proveniência autenticada serem homologados.

---

## Atualização operacional — 27/11/2026, 01:16 BRT

**Esta seção é a leitura mais recente desta execução e substitui os números anteriores quando divergirem.**

### Render

- Workspace: My Workspace.
- PostgreSQL Render: a listagem retorna **0 instâncias**; o ID `dpg-db2h93h7lnhs73ev17og-a` continua retornando HTTP 404.
- Wero1Mercados produção: serviço `srv-db2fvq4s728c73cahjq0`, branch `main`, plano Free, auto-deploy ligado, health check vazio, não suspenso no painel; eventos registram falhas de servidor com exit code 3.
- Logs mais recentes, 27/11 01:14 BRT: startup chama `init_db()`, falha ao resolver o host do PostgreSQL antigo e encerra. Evento `server_failed` registrado às 01:14 BRT. Foram retornados 11 eventos `server_failed` na janela consultada de 24 horas.
- Wero1Mercados staging: branch `dev/p0-provider-reconciliation-20261012`, auto-deploy desligado, health check vazio; nenhum evento ou log na janela de 24h.
- Wero1Divulgação staging: branch `feat/wero1divulgacao-bootstrap`, auto-deploy desligado, health check vazio; nenhum evento ou log na janela de 24h.
- Nenhum teste HTTP de `/go/` ou `/out/` foi executado: o Render staging continua no branch antigo e as rotas anteriores podem gerar efeitos colaterais. A validação fica limitada ao código candidato e CI.

### Neon

- Produção (`long-tooth-35390946`, branch `br-spring-hall-b5ed425u`): zero tabelas públicas, zero snapshots e schedule vazio.
- Staging (`floral-hat-53843763`, branch `br-autumn-salad-b4cg34pj`): 15 tabelas públicas, zero snapshots e schedule vazio.
- SQL read-only confirmou `product_offers` = 19 registros, 19 ativos, 0 disponíveis, 0 verificados pelo provedor, 0 com preço positivo, 0 com comissão positiva, 0 atualizados nos últimos 7 dias.
- `offers` = 20; `partners` = 2.
- Cliques, conversões, tokens outbound, auditoria de conversão, ledger, visitas landing/catalog = 0.
- `ops_persistence_probe` = **58 registros**; último probe `paradigma-iter11-20261127-0018-bst`, em 27/11 00:20:52 BRT. Não foi criado probe nesta execução.

### Metricool — consulta desta execução

- Brand NeyMareSol (7259526), Instagram conectado `@neymaresoloficial`, diferente de `@neymaresol`; Facebook e TikTok conectados.
- Posts agendados entre 27/11 01:16 e 04/12 23:59 BRT: **0**.
- Horários sugeridos para sexta, 27/11: Facebook 10h (score 12.767); TikTok 10h (1.379) e 18h (1.222); Instagram scores 0. São apenas sugestões de plataforma, não garantias.
- Nenhuma publicação criada, enviada ou agendada. SmartLinks/atribuição comercial não foram novamente consultados nesta execução.

### GitHub e Double Check

- PR #98 Wero1Mercados: aberta, Draft, sem merge, HEAD `8e1f13a0b8f515869d214ebb6947eee5eb88cf44`; os quatro workflows associados concluíram `success`. Status check combinado não retornou entries; os workflows listados são a evidência CI disponível.
- PR #95 Shopee: permanece aberta/Draft e contém helper que aceita `source_authenticated=True` e scores em mapping fornecido pelo chamador. Não mesclar separadamente; consolidar apenas com gate fail-closed da #98.
- PR #50 Wero1Divulgação: aberta/Draft, sem merge; dois workflows associados concluíram `success`.
- PR #51 permanece aberta/Draft; esta atualização é documental e não altera runtime, configuração, banco, ranking ou catálogo.

### Limites

- Persistência comprovada apenas no Neon staging; nenhum backup restaurável demonstrado.
- Nenhuma conexão Render↔Neon staging ou produção comprovada.
- Nenhuma venda, comissão ou pagamento comprovado; todos os contadores comerciais consultados estão zerados.
- Sem merge, deploy, gasto, anúncio, publicação ou evento comercial sintético.
- Wero1Operário e Wero1Elétrico não foram alterados.

**Decisão atual: HOLD.** Recuperação/migração do banco, backup restaurável, conexão isolada de staging, segredo HMAC, homologação de health e funil, fonte autenticada de conversões e rollback continuam obrigatórios antes da promoção.


## Sinal público complementar — Senacon (verificado em 27/11/2026)

- **Notificação preventiva (18/11/2026):** a Senacon solicitou informações de Amazon, Mercado Livre, TikTok Shop/ByteDance, Shopee, Temu e Instituto para Desenvolvimento do Varejo sobre prevenção de descontos artificiais, correspondência entre oferta e checkout, identificação de publicidade patrocinada/afiliados, selos de loja oficial/vendedor verificado, contadores regressivos, escassez, serviços extras, cancelamento, arrependimento e reembolso. [Fonte oficial](https://www.gov.br/mj/pt-br/assuntos/noticias/senacon-notifica-plataformas-e-varejistas-para-prevenir-problemas-durante-a-black-friday)
- **Cartilha on-line (25/11/2026):** comparar o total com frete, taxas e juros; verificar URL oficial e reputação; confirmar beneficiário Pix/boleto; guardar anúncio, comprovantes e protocolo; evitar falsa urgência; direito de arrependimento de 7 dias para compras on-line, conforme a cartilha. [Fonte oficial](https://www.gov.br/mj/pt-br/assuntos/noticias/senacon-lanca-cartilha-com-orientacoes-para-compras-seguras-na-black-friday)

**Aplicação editorial Werozinha:** identificar publicidade/links afiliados claramente; não usar selo “loja oficial”/“vendedor verificado” sem comprovação; não declarar desconto ou escassez sem fonte datada; exibir vendedor, preço, frete, prazo e condições apenas quando verificados. Os sinais permanecem editoriais — não alimentam catálogo, ranking, INT.1/INT.2, conversões, comissões ou pagamentos.


## Render — métricas e deploy (consulta posterior, 27/11/2026 01:20 BRT)

- Último deploy Live de Wero1Mercados: 23/10/2026 10:34 BRT, commit `80018a1c3b4a41d8bb052ddf798b11b10d613afa`; histórico não mostrou novo deploy nesta consulta.
- Métricas do serviço produção na janela 26/11 19:00–27/11 01:20 BRT: uma série de memória com amostra 3.190.784 bytes às 01:20; CPU, instâncias, requisições HTTP e latência sem séries.
- Métricas Wero1Mercados staging e Wero1Divulgação staging: CPU, memória, instâncias, HTTP e latência sem séries.
- A leitura não autoriza deploy nem prova que o health HTTP está acessível.
