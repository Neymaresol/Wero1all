# Wero1 Operário v1.2.0 — Auto Catalog
Versão: 2026-09-29 BRT

- Busca automática via API oficial Hotmart.
- POST /api/catalog/scan (WERO_ADMIN_TOKEN).
- GET /api/catalog.
- HOTMART_ACCESS_TOKEN apenas no Render.
- Preserva ledger e deduplicação da v1.1.2.
- Não cria produtos, compradores ou vendas.

Limite: a documentação oficial atual descreve GET /products/api/v1/products como catálogo do creator, não como Mercado de Afiliação. Por isso esta versão não inventa nem converte links de creator em HotLinks de afiliado. A ativação comercial automática só deve ocorrer quando uma interface oficial/autorizada retornar a afiliação e o HotLink da conta.
