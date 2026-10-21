# PARADIGMA — Expansao do catalogo Hotmart
Versao: plano-dev-1 | Ultima revisao: 2026-10-21 13:07 America/Sao_Paulo
Escopo: somente desenvolvimento. Nenhuma alteracao em producao.

## Objetivo
Ampliar catalogo Hotmart por todos os nichos compatíveis com os robos PARADIGMA, com comissao minima desejada de 20%, Brasil primeiro e expansao internacional posterior. Priorizar ofertas com afiliacao aprovada e HotLink do titular.

## Evidencia atual
- Conta Hotmart: 3 afiliacoes confirmadas por capturas do titular: 232173 Curso Lembrancinhas e Flores em E.V.A; 42903 LeadLovers; 2084310 Viva Sempre com Dinheiro.
- HotLink LeadLovers informado pelo titular: https://go.hotmart.com/O107910953Y. Navegacao ate pagina de vendas observada, mas atribuicao financeira nao validada.
- HotLinks dos outros dois produtos: PENDENTE.
- Comissao percentual dos tres: NAO VERIFICADA; nao presumir >=20%.
- Relatorio Hotmart de 21/09/2026 a 21/10/2026: 0 transacoes visiveis no filtro da captura.
- Wero1all/main.py VERSION 1.9.0 tem offers, catalog_products, transactions, campaign_clicks e configuracao Hotmart (HOTTOK, access token). Configuracao nao comprova API funcional.
- Wero1Mercados tem catalog_discovery.py, ai_acquisition.py, paradigma_tags.py e integracoes Shopee; verificar contrato de integracao antes de reuso.
- Metricool marca 7259526: Facebook, Instagram neymaresoloficial, TikTok neymaresoltiktok; agendamentos 21-28 outubro: nenhum.

## Pipeline proposto (nao habilitado)
1. Discovery: fontes publicas/oficiais permitidas; respeitar limites e termos, sem scraping autenticado, sem burlar acesso.
2. Normalizacao: provider, product_id, titulo, nicho, idioma, pais, preco, moeda, percentual de comissao, origem, data de verificacao.
3. Autorizacao: approved / pending / rejected / unknown; somente approved pode seguir. Comissao desconhecida => pending.
4. Gate comercial: comissao >=20%, HotLink oficial individual do titular, destino permitido, elegibilidade territorial, regras do produtor, politica da rede, revisao de alegacoes.
5. Roteamento por robo e mercado: BR/pt-BR primeiro; internacional apenas apos validacao de idioma, checkout e regras.
6. Campanhas: IA cria variantes, revisao humana/canal autorizado, rate limits, nao gerar cliques artificiais, nao enviar spam.
7. Medicao: separar impressoes/visitas/cliques de vendas e comissoes autenticadas pelo provedor; auditoria, deduplicacao, reversoes.

## Double Check antes de qualquer deploy
- Testes de elegibilidade: aprovado + >=20% + HotLink autentico => elegivel; qualquer requisito ausente => bloqueado.
- Testes de entrada maliciosa, URLs nao autorizadas, duplicatas, reversoes, privacidade e origem das evidencias.
- Testes de campanha por canal e idioma com fixtures; sem publicacao externa.
- Banco temporario isolado (SQLite ou PostgreSQL de teste), nunca usar banco efetivo de producao.
- Health, logs sem segredos, canary e rollback documentado; nenhum merge automatico.
- Revisao de propriedade do HotLink, comissoes e autorizacoes reais pelo titular.

## Bloqueios P0
P0-1: inexistencia de HotLinks verificados para 232173 e 2084310.
P0-2: percentual de comissao nao confirmado para os 3 produtos.
P0-3: API de descoberta global do Mercado de Afiliacao nao comprovada; nao assumir acesso a todos os produtos.
P0-4: atribuicao/conciliacao de vendas e comissoes requer comprovacao da Hotmart.
P0-5: canais sociais e identidade do Instagram precisam de revisao antes de publicar.

## Condicao de liberacao
Apenas PR revisado, testes aprovados, staging isolado, Double Check, autorizacao explicita de deploy e rollback pronto.