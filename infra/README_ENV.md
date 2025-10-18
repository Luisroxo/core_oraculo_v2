# Variáveis de Ambiente e Secrets — ORÁCULO v2.0

Este arquivo documenta as principais variáveis de ambiente utilizadas no projeto. Use o arquivo `env.example` como base para criar seu `.env` local.

## Como usar
1. Copie o arquivo `infra/env.example` para `infra/.env`.
2. Preencha os valores conforme seu ambiente (desenvolvimento, produção, etc).
3. Os serviços Docker podem ser configurados para carregar automaticamente o `.env`.

## Variáveis principais

### API Gateway
- `API_GATEWAY_HOST`: Host de escuta do gateway (padrão: 0.0.0.0)
- `API_GATEWAY_PORT`: Porta do gateway (padrão: 8000)
- `API_GATEWAY_SECRET_KEY`: Chave secreta para autenticação/JWT

### Orquestrador
- `ORQUESTRADOR_HOST`: Host do orquestrador
- `ORQUESTRADOR_PORT`: Porta do orquestrador

### Banco de Dados
- `POSTGRES_USER`: Usuário do banco
- `POSTGRES_PASSWORD`: Senha do banco
- `POSTGRES_DB`: Nome do banco
- `POSTGRES_HOST`: Host do banco (use o nome do serviço Docker)
- `POSTGRES_PORT`: Porta do banco

### Redis
- `REDIS_HOST`: Host do Redis
- `REDIS_PORT`: Porta do Redis

### RabbitMQ
- `RABBITMQ_HOST`: Host do RabbitMQ
- `RABBITMQ_PORT`: Porta do RabbitMQ
- `RABBITMQ_DEFAULT_USER`: Usuário padrão
- `RABBITMQ_DEFAULT_PASS`: Senha padrão

### Microsserviços Escavadores
- `YOUTUBE_API_KEY`: Chave de API do YouTube
- `BLOG_API_URL`: URL da API do Blog
- `TELEGRAM_BOT_TOKEN`: Token do bot Telegram
- `INSTAGRAM_API_KEY`: Chave de API do Instagram
- `LICITACOES_API_URL`: URL da API de Licitações

### Executadores
- `RELATORIOS_OUTPUT_PATH`: Caminho de saída dos relatórios
- `CONTEUDO_IA_API_KEY`: Chave de API para IA
- `MIDIAS_SOCIAIS_TOKEN`: Token de integração de mídias sociais
- `AUTOMACOES_CONFIG_PATH`: Caminho de configs de automações
- `ERP_CRM_URL`: URL do ERP/CRM

## Boas práticas
- Nunca versionar arquivos `.env` com dados sensíveis.
- Use variáveis diferentes para ambientes de dev, staging e produção.
- Secrets devem ser gerenciados por cofre de segredos em produção (ex: AWS Secrets Manager, Azure Key Vault).

---
Dúvidas? Consulte este arquivo ou o time de DevOps.