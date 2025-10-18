# Roadmap do Core ORÁCULO v2.0

## 1. Planejamento e Arquitetura
- [x] Definir estrutura de pastas e organização do repositório
- [x] Escolher tecnologias principais (FastAPI, RabbitMQ, Redis, PostgreSQL, Docker, K8s)
- [x] Definir padrões de microsserviços, comunicação e versionamento de API
- [x] Elaborar diagrama de arquitetura detalhado
- [x] Definir estratégia de versionamento de código (Git Flow, trunk-based, etc.)
- [x] Planejar governança de dados e compliance (LGPD, backups, retenção)

- [x] Criar arquivos Dockerfile para todos os serviços
- [x] Criar docker-compose para ambiente local
- [x] Setup de ambiente local automatizado (Makefile ou scripts)
- [x] Definir variáveis de ambiente e secrets (env.example)
- [x] Documentação de onboarding e setup rápido
- [x] Configurar pré-commit hooks (lint, format, security)

## 3. Desenvolvimento de Serviços
- [x] Implementar API Gateway (FastAPI)
    - [x] Autenticação JWT/OAuth2
    - [x] Roteamento e versionamento de endpoints
    - [x] Rate limiting
    - [x] Monitoramento e logs
- [ ] Desenvolver Orquestrador Core
	- [x] Orquestração de escavadores e executadores
		- [x] [ ] Definir stack oficial do orquestrador (Python, FastAPI, Celery, RabbitMQ, Redis, Prometheus, ELK)
		- [x] [ ] Especificar padrão de mensagens (JSON, correlation_id, tipo_evento, payload, timestamp)
		- [x] [ ] Documentar fluxo de orquestração (iniciar_coleta, resultado_coleta, iniciar_execucao, resultado_execucao)
		- [x] [ ] Definir contratos de integração (escavadores, executadores, orquestrador)
		- [x] [ ] Estratégias de escalabilidade, monitoramento e logs
		- [x] [ ] Exemplo de código de task Celery
	- [x] Distribuição de tarefas e agregação de resultados
	- [x] Interface com mensageria
	- [x] Criar microsserviços Escavadores
	- [ ] YouTube
	- [ ] Blog
	- [ ] Telegram
	- [ ] Instagram
	- [ ] Licitações
- [ ] Criar microsserviços Executadores
	- [ ] Relatórios
	- [ ] Conteúdo (IA)
	- [ ] Mídias Sociais
	- [ ] Automações
	- [ ] ERP/CRM

## 4. Integração, Testes e Qualidade
- [ ] Escrever testes unitários para todos os serviços
- [ ] Escrever testes de integração (end-to-end)
- [ ] Configurar cobertura de testes (coverage)
- [ ] Configurar análise estática de código (lint, type check)
- [ ] Revisão de código (pull requests obrigatórios)
- [ ] Automatizar build e testes no CI

## 5. Infraestrutura, Deploy e Observabilidade
- [ ] Implementar Data Lake / Repositório Central (MongoDB/PostgreSQL/MinIO/S3)
- [ ] Configurar mensageria/event bus (RabbitMQ/Redis Streams/NATS)
- [ ] Configurar Prometheus, Grafana e ELK Stack para monitoramento
- [ ] Centralizar logs, métricas e alertas
- [ ] Criar pipelines CI/CD no GitHub Actions
- [ ] Scripts de build, test, deploy e rollback
- [ ] Integração com Docker, K8s e Helm
- [ ] Estratégia de rollback e deploy seguro

## 6. Segurança e Boas Práticas
- [ ] Implementar autenticação e autorização robustas
- [ ] Gerenciar secrets e variáveis sensíveis
- [ ] Análise de vulnerabilidades (dependabot, bandit, etc.)
- [ ] Políticas de backup e disaster recovery
- [ ] Documentar políticas de segurança e privacidade

## 7. Documentação e Governança
- [ ] Documentação técnica dos serviços e APIs (OpenAPI/Swagger)
- [ ] Documentação de uso para clientes internos/externos
- [ ] Manuais de operação e troubleshooting
- [ ] Políticas de versionamento e ciclo de vida dos serviços

## 8. Manutenção e Evolução
- [ ] Planejar rotinas de atualização de dependências
- [ ] Monitorar performance e custos
- [ ] Coletar feedback dos usuários e stakeholders
- [ ] Planejar roadmap de evolução contínua
