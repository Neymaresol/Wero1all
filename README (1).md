# Wero1 Operário — Deploy Package
Última versão: 2026-09-28 (BRT)

Pacote de implantação do núcleo operacional e monitor Wero1Status.

## Incluído
- FastAPI backend
- `/health` para health check
- `/api/status` para consolidação PAI/FILHOS
- `/webhooks/{provider}` para ingestão normalizada e idempotente
- SQLite local para validação inicial
- Dashboard Wero1Status
- Dockerfile + render.yaml
- `.env.example` sem segredos

## Regra financeira
Dados só entram nos totais reais quando `confirmed=true`. O endpoint normalizado não substitui a validação de assinatura nativa de Asaas/Hotmart/Kiwify: adapters de produção devem validar a assinatura do provedor antes de enviar o evento ao núcleo.

## Deploy no Render
1. Suba estes arquivos para a raiz do repositório GitHub.
2. Crie um Web Service/Blueprint usando `render.yaml`.
3. Configure as credenciais reais exclusivamente como Secrets/Environment Variables no Render.
4. Faça deploy e valide `/health`.
5. Só marque PRODUÇÃO/OK depois de health check, webhook de teste, idempotência e evento real confirmado pelo provedor.

## Observação de persistência
SQLite serve para validação inicial. Para produção com múltiplas instâncias/workers, migre para PostgreSQL antes de escalar.
