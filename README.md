# Wero1 Operário v1.1.0
Atualização preparada em 29/09/2026.

## Objetivo
Manter o Wero1 em produção e acrescentar base para vendas digitais Hotmart sem OpenAI API nesta fase.

## Recursos
- Webhook Hotmart protegido por HOTMART_HOTTOK
- Idempotência por event_id
- Eventos de funil, venda e reversão
- Catálogo local de ofertas/HotLinks
- /health, /api/status, /api/funnel e /api/offers
- Dashboard simples com atualização automática

## Configuração obrigatória no Render
HOTMART_HOTTOK = token Hottok configurado na Hotmart
DB_PATH = /app/data/wero1.db
WERO_MODE = production

Nunca coloque tokens/chaves diretamente no GitHub.

## Antes do GO
1. Fazer backup da versão atual.
2. Subir estes arquivos no repositório.
3. Confirmar HOTMART_HOTTOK no Render.
4. Aguardar deploy e abrir /health.
5. Confirmar version=1.1.0 e status=ok.
6. Testar webhook Hotmart.
7. Só contabilizar venda real após evento válido da Hotmart.

Observação: esta versão não cria tráfego nem garante vendas. Ela fornece infraestrutura de ofertas, rastreamento e confirmação para o funil comercial.
