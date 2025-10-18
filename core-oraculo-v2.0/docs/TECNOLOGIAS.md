# Tecnologias Principais do Core ORÁCULO

## API Gateway
- FastAPI (Python)
- Autenticação JWT/OAuth2
- Rate limiting: FastAPI-limiter ou custom
- Monitoramento: Prometheus, logs estruturados

## Orquestrador e Microsserviços
- FastAPI (Python) para APIs
- RabbitMQ (mensageria principal)
- Redis (cache, filas rápidas, locks)
- PostgreSQL (banco relacional principal)
- MongoDB (data lake, dados não estruturados)
- MinIO/S3 (armazenamento de arquivos)

## Infraestrutura
- Docker (containerização)
- Docker Compose (ambiente local)
- Kubernetes (K8s) para orquestração em produção
- GitHub Actions (CI/CD)
- Helm (deploy K8s)

## Observabilidade
- Prometheus (métricas)
- Grafana (dashboards)
- ELK Stack (logs centralizados)

## Padrões de Microsserviços
- Comunicação assíncrona via RabbitMQ
- APIs RESTful (FastAPI)
- Configuração por variáveis de ambiente
- Deploy independente por serviço
- Testes automatizados (pytest)
- Versionamento de API

---

> Esta lista pode ser expandida conforme a evolução do projeto e integrações específicas de cada escavador/executador.
