# PARADIGMA — Plano de correção comercial (Double Check)

Data: 2026-10-11 (BRT). Status: branch isolada, sem deploy.

## Critérios de aceitação

1. Separar health/deploy de status comercial. Não inferir vendas a partir de HTTP 200.
2. Contabilizar visitas humanas e cliques de afiliado com IDs, origem, campanha, robô e timestamp; filtrar probes e deduplicar eventos.
3. Expor diagnóstico somente leitura com totais de ofertas ativas e aprovadas, visitas, cliques, publicações verificadas, conversões pendentes e vendas confirmadas.
4. Registrar publicação somente após confirmação da plataforma de destino (ID, URL e data). Agendamento não equivale a publicação.
5. Reconciliar transações por evento autenticado do parceiro, com idempotência, estornos e testes excluídos; nunca fabricar comissões.
6. Verificar autorização e domínio HTTPS dos links de afiliado; não expor ofertas sem aprovação.
7. Validar banco persistente, backups, falhas e alarmes; evitar qualquer escrita em produção durante auditoria.
8. Testar em staging: unitários, integração, smoke, Double Check e rollback antes de propor merge.

## Evidências pendentes

- Leitura dos corpos atuais das APIs de aquisição e comercial.
- Identificadores reais de publicação nas redes e métricas dos canais.
- Reconciliação financeira autenticada Amazon/Hotmart.
- Testes de ponta a ponta com tráfego real autorizado.

Não habilitar campanhas, não realizar merge nem deploy automaticamente.
