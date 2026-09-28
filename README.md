# Wero1Status
Monitor web do Wero1 Operário e sua hierarquia PAI/FILHOS.

## Regra financeira principal
Nenhum valor é considerado transferência real sem confirmação do provedor financeiro. Projeções, simulações e valores pendentes devem permanecer separados.

## Executar localmente
No diretório Wero1Status execute: `python3 -m http.server 8080` e abra `http://localhost:8080`.

## Integração de produção
O frontend está preparado para receber uma lista de robôs do backend. Em produção, conectar via WebSocket ou SSE a um serviço que consuma webhooks/APIs oficiais (ex.: provedor de pagamentos e plataformas de venda), valide assinatura/idempotência e persista eventos antes de publicar no dashboard.

Campos por robô: id, name, parent, status, sales, gross, commission, balance, transferred, transferConfirmed, lastEvent.
