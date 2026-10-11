# PARADIGMA P0 — plano de implantação segura
Data: 2026-10-11. Estado: SOMENTE DESENVOLVIMENTO; sem merge/deploy.

## Double Check obrigatório
1. Confirmar serviço Render, branch, variáveis de conexão **apenas por nomes e fingerprints redigidos**; nunca imprimir senhas, URLs completas ou tokens.
2. Executar inventário SQL somente leitura: current_database(), current_schema(), pg_namespace e contagem de linhas por tabela comercial; conferir banco correto e origem do dashboard.
3. Wero1 Operário: verificar se /app/data está montado em disco persistente no serviço efetivo. render.yaml não comprova montagem. Antes de migração, exportar snapshot criptografado e validar restauração em ambiente isolado.
4. Wero1Mercados: conferir DATABASE_URL no serviço efetivo, tabela offers, clicks, offer_landing_visits, transações/eventos e regras de atribuição; sem escrever dados.
5. Wero1Elétrico: conferir WERO_ELETRICO_DATABASE_URL, database wero1eletrico, schema wero1eletrico, tabelas offers/events e aprovação de ofertas; não liberar campanhas.
6. Testes: python -m pytest -q tests/test_p0_*.py (onde presentes); executar também smoke HTTP GET/HEAD em staging, verificação de integridade e reconciliação de eventos autenticados.
7. Backup: snapshot do banco de origem + hash SHA-256, contagens por tabela, registro UTC, retenção e teste de restauração em ambiente isolado. Não armazenar dados reais no GitHub.
8. Rollback: manter versão atual e banco original intactos; somente promover nova versão após autorização expressa, testes, health, canary e monitoramento. Reverter tráfego e conexões se falhar; não aplicar migrations destrutivas.

## Critérios GO
- Identidade do banco e schema comprovada para cada robô.
- Nenhuma venda sintética; apenas confirmações autenticadas e reconciliadas.
- Preservação de histórico e ausência de perda de dados demonstradas.
- Testes automatizados e restauração de backup aprovados.
- Aprovação humana explícita para merge e deploy.

## Situação
Este arquivo é documentação preparatória. Não confirma backup executado, restauração validada nem correção aplicada.
