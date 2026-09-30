# Wero1 Operário v1.1.2
Atualização de segurança e integridade financeira.

## Mudanças
- Deduplicação por `event_id` e consolidação financeira por `transaction_id` Hotmart.
- `PURCHASE_APPROVED` + `PURCHASE_COMPLETE` da mesma transação contam uma única venda.
- Refund/chargeback/cancel/expired marcam a transação como revertida.
- `PURCHASE_PROTEST` e payloads identificados como teste não entram nas vendas financeiras.
- Métricas `/api/status` passam a usar o ledger `transactions`, isolando os eventos antigos de teste da v1.1.1.
- `POST /api/offers` protegido por `Authorization: Bearer <WERO_ADMIN_TOKEN>`.
- Mantém Hottok no header `X-HOTMART-HOTTOK`.

## Render
Mantenha `HOTMART_HOTTOK` e configure uma nova variável secreta `WERO_ADMIN_TOKEN` com um valor forte gerado no próprio Render/gerenciador de segredos. Não coloque segredos no GitHub.

## Após deploy
1. Abra `/health` e confirme version 1.1.2, Hottok true e admin token true.
2. Reenvie somente um evento Hotmart conhecido e confira HTTP 200.
3. Confira `/api/funnel`.
4. Confira `/api/status`: eventos de teste antigos não devem aparecer como vendas.
5. Cadastre ofertas SOMENTE com HotLinks reais/autorizados usando o token administrativo.

## Importante
Esta versão não fabrica compradores e não inventa produtos/HotLinks. Tráfego deve vir de canais legítimos e ofertas autorizadas. Comissão, saldo e transferência permanecem zero até integração/reconciliação financeira específica com a fonte oficial.
