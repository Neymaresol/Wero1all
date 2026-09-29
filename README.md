# Wero1 Operário v1.0.2 — Hotmart Webhook 2.0
Última versão: 29/09/2026 06:21 (Brasil, UTC-3).

Correções:
- Hotmart 2.0: id/event/data.
- PURCHASE_APPROVED é o único evento contado como venda confirmada.
- Idempotência evita duplicação em retentativas.
- HOTMART_HOTTOK fica somente no ambiente do Render.
- Disco persistente configurado em /app/data.

Após upload no GitHub:
1. Fazer/aguardar redeploy no Render.
2. Configurar HOTMART_HOTTOK no Render, sem publicar o segredo.
3. Confirmar /health com version 1.0.2.
4. Reprocessar um evento Hotmart e buscar HTTP 2xx.
5. Eventos de teste não são vendas reais.
