# Padrões de Microsserviços, Comunicação e Versionamento de API

## Microsserviços
- Cada serviço deve ser pequeno, focado em um domínio de negócio e independente para deploy.
- Comunicação entre microsserviços preferencialmente assíncrona (eventos/mensageria), mas REST/gRPC para integrações síncronas.
- Cada serviço deve ter seu próprio repositório de dados (Database per Service).
- Serviços devem ser stateless (sem estado persistente em memória).
- Utilizar contratos de API bem definidos (OpenAPI/Swagger).
- Versionamento de serviços e APIs obrigatório.
- Observabilidade: logs estruturados, métricas e tracing distribuído.

## Comunicação
- REST para APIs públicas e integrações simples.
- gRPC para comunicação interna de alta performance.
- Mensageria (RabbitMQ, Redis Streams, NATS) para eventos e processamento assíncrono.
- Padrão de mensagens: eventos imutáveis, com versionamento e schema registry quando necessário.
- Utilizar correlation ID para rastreabilidade entre serviços.

## Versionamento de API
- Versionamento via URL (ex: /v1/endpoint) ou header (ex: Accept: application/vnd.oraculo.v2+json).
- Mudanças incompatíveis exigem nova versão da API.
- Documentar todas as versões disponíveis e ciclo de vida (depreciação, sunset).
- Utilizar ferramentas como Swagger/OpenAPI para documentação e validação.

## Boas Práticas Gerais
- Testes automatizados para contratos de API (contract tests).
- Monitoramento de erros e performance por serviço.
- Deploy independente e pipelines CI/CD por serviço.
- Políticas de rollback e deploy seguro.
- Segurança: autenticação, autorização e validação de payloads em todos os endpoints.

---

Este documento serve como referência para padronização dos microsserviços do Core ORÁCULO v2.0. Atualize conforme o projeto evoluir.