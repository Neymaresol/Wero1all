# Wero1 Operário v1.1.1 — Correção de Deploy

Data: 29/09/2026

Correção principal:
- O Render falhava com `"/static": not found`.
- O Dockerfile agora cria `/app/static` durante o build e copia o `index.html`
  da raiz do repositório para `/app/static/index.html`.
- Assim o deploy não depende da existência prévia da pasta `static` no GitHub.

Mantido:
- Catálogo de ofertas/HotLinks.
- Funil Hotmart.
- Eventos de venda aprovada/completa.
- Reembolso, chargeback, cancelamento e expiração.
- Deduplicação de eventos.
- Validação HOTMART_HOTTOK.
- OpenAI API continua fora desta versão.

Após subir os arquivos na raiz do GitHub, execute no Render:
Manual Deploy > Deploy latest commit

Resultado esperado em /health:
`"status":"ok"` e `"version":"1.1.1"`.
