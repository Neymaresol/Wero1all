# Wero1Divulgação — PARADIGMA

Versão de projeto: 0.1.0-dev
Registro: 2026-10-13 17:49 America/Sao_Paulo (horário de referência da solicitação; não é horário de deploy)
Estado: especificação inicial, NÃO implantado.

## Responsabilidades
- Centralizar criação, aprovação, agendamento e análise de campanhas de Wero1Mercados, Wero1Operário e Wero1Elétrico.
- Os três robôs comerciais preservam catálogo, aprovação de ofertas, redirecionamentos, atribuição, conciliação de vendas e comissões.
- Nunca criar ofertas, preços, comissões, vendas ou cliques sintéticos.
- Usar somente ofertas aprovadas, links autorizados e identificadores de campanha por robô e plataforma.

## Fluxo
1. Ler APIs comerciais com credenciais de escopo mínimo, preferencialmente somente leitura.
2. Selecionar ofertas autorizadas e verificar destino HTTP e regras de parceiros.
3. Preparar mídia, legenda, declaração de conteúdo comercial e chamada para a vitrine.
4. Double Check de criativo, direitos, marca, URL, rastreio e política da rede.
5. Publicar/agendar somente em contas explicitamente autorizadas e conectadas via APIs oficiais; iniciar com revisão humana.
6. Medir impressões, visitas e cliques com proveniência, separar de conversões confirmadas pelo parceiro.
7. Comparar resultados e propor ajustes sem ultrapassar limites de gasto.

## Canais
- Metricool detectado: TikTok neymare soltiktok (nome exato: neymaresoltiktok), Instagram neym aresoloficial (nome exato: neymaresoloficial), Facebook conectado.
- Conta desejada Instagram @neymaresol não corresponde à conexão atual: BLOQUEAR publicação nesse perfil até reconexão/validação.
- Kwai: conector oficial e permissão ainda não confirmados; não automatizar por scraping ou bot de interface.
- TikTok pode exibir aviso de site externo; não há garantia de bypass.
- Vídeos comuns não contêm regiões clicáveis arbitrárias; CTA clicável depende do formato de anúncio e permissões da plataforma.

## Gates obrigatórios antes do GO
- Isolamento staging/produção, secrets fora do Git, RBAC, logs sem tokens.
- Permissão da conta e da plataforma; consentimento explícito para gastos e limite de orçamento.
- Testes de idempotência, rate limit, falha de API, retentativa com backoff, kill switch, rollback.
- Saúde do scheduler, fila e publicações confirmadas pelo provedor.
- Painel por robô: campanha, canal, publicação, visitas, cliques, vendas confirmadas, comissões confirmadas e falhas; não inferir vendas de telemetria.
- Double Check e aprovação antes de habilitar postagem autônoma.

## Limites desta alteração
Somente documentação na branch de desenvolvimento. Sem merge, sem deploy, sem postagem, sem mudança de produção.
