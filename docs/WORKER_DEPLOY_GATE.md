# Wero1 Operário — Worker real (implantação separada)

Data: 2026-10-09 (horário de Brasília). Versão de aplicação existente: 1.9.0.

O script `scripts/heartbeat_worker.py` **não** é iniciado pelo serviço web. Implantá-lo requer um serviço worker separado no Render ou executor externo, para evitar execução duplicada por múltiplos web instances. **Não** contém automação de publicidade, disparos de campanhas, compra, cliques ou vendas.

Variáveis: `WERO_BASE_URL=https://wero1all.onrender.com`, `WERO_ADMIN_TOKEN` (segredo já configurado no serviço web, copiar com segurança, não publicar), `WERO_ROBOT_ID=WERO1-PAI`, `WERO_HEARTBEAT_INTERVAL=60`. Comando: `python scripts/heartbeat_worker.py`.

**Gate antes do GO**: (1) verificar autenticação e resposta 2xx; (2) observar `/api/robots/heartbeats` com `heartbeat_fresh_count=1` enquanto processo estiver ativo; (3) parar worker e confirmar expiração em 180 segundos; (4) verificar reinício e logs sem vazamento de token; (5) habilitar persistência Neon antes de declarar histórico confiável após deploy. A API atualmente grava heartbeat em SQLite local efêmero.

**Importante**: Render Background Worker pode exigir plano pago. Não provisionar nem alterar plano sem autorização expressa. Worker não confirma execução comercial ou vendas. Wero1Mercados é independente e não deve ser alterado.
