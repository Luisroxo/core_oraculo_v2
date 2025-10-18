# Arquitetura do Core ORÁCULO v2.0

## Visão Macro

```mermaid
graph TD
      Usuario[Usuário SaaS] --> Frontend
      Frontend[Frontend (React/Next.js)] --> APIGateway
      APIGateway[API Gateway (FastAPI)] --> Orquestrador
      Orquestrador[Orquestrador Core] --> Escavadores
      Orquestrador --> Executadores
      Escavadores[Escavadores (YouTube, Blog, Telegram, Instagram, Licitações)] --> DataLake
      Executadores[Executadores (Relatórios, Conteúdo IA, Mídias Sociais, Automações, ERP/CRM)] --> DataLake
      Orquestrador --> Mensageria
      Mensageria[(RabbitMQ, Redis Streams, NATS)] --> Escavadores
      Mensageria --> Executadores
      DataLake[(MongoDB, PostgreSQL, MinIO/S3)]
      APIGateway --> Auth[Autenticação JWT/OAuth2]
      Orquestrador --> Monitoramento[Prometheus, Grafana, ELK]
      Todos --> CI_CD[CI/CD (GitHub Actions, Docker, K8s, Helm)]
```

## Padrões de Microsserviços
- Serviços pequenos, focados em domínio, independentes para deploy.
- Comunicação preferencialmente assíncrona (eventos/mensageria), REST/gRPC para integrações síncronas.
- Banco de dados por serviço (Database per Service).
- Stateless e contratos de API bem definidos (OpenAPI/Swagger).
- Versionamento obrigatório de serviços e APIs.
- Observabilidade: logs estruturados, métricas e tracing distribuído.

## Comunicação
- REST para APIs públicas e integrações simples.
- gRPC para comunicação interna de alta performance.
- Mensageria (RabbitMQ, Redis Streams, NATS) para eventos e processamento assíncrono.
- Eventos imutáveis, versionados, com correlation ID para rastreabilidade.

## Versionamento de API
- Versionamento via URL (ex: /v1/endpoint) ou header.
- Mudanças incompatíveis exigem nova versão.
- Documentação e ciclo de vida de APIs (depreciação, sunset).

## Observabilidade e DevOps
- Monitoramento centralizado (Prometheus, Grafana, ELK).
- Pipelines CI/CD por serviço (GitHub Actions, Docker, K8s, Helm).
- Deploy independente, rollback seguro e automação de build/test/deploy.

## Segurança
- Autenticação e autorização robustas (JWT/OAuth2).
- Gestão de secrets e variáveis sensíveis.
- Análise de vulnerabilidades automatizada.

---

Consulte o roadmap e o arquivo PADROES_MICROSSERVICOS.md para detalhes e evolução dos padrões.
```