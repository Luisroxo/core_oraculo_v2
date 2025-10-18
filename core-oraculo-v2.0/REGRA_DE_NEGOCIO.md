# Regra de Negócio Oráculo — Agente Escavador de Dados

> Documento convertido do PDF original para Markdown.

## 1. Visão Geral
O Oráculo é uma plataforma SaaS para coleta, análise e entrega de dados públicos, automatizando processos de extração, transformação e disponibilização de informações para usuários de diferentes perfis (Admin, Analista, Viewer).

## 2. Perfis de Usuário
- **Admin:** Gerencia usuários, planos, permissões e configurações gerais.
- **Analista:** Agenda coletas, acessa relatórios, configura integrações.
- **Viewer:** Visualiza relatórios e dashboards.

## 3. Módulos Principais
- **Frontend (UI):** React/Next.js, Tailwind, comunicação via API Gateway.
- **API Gateway:** FastAPI, autenticação centralizada (JWT/OAuth2), roteamento, monitoramento.
- **Microsserviços:**
  - Usuários: Cadastro, login, planos, permissões.
  - Coletas: Agendamento, execução de scrapers, monitoramento.
  - Relatórios: Geração automática (PDF, CSV), dashboards.
  - Notificações: Alertas via email, webhook, SMS.
  - Integrações: APIs externas (YouTube, ComprasNet, etc.), atualização de tokens.
- **Mensageria/Event Bus:** RabbitMQ, Redis Streams ou NATS para comunicação assíncrona.
- **Infraestrutura:** Docker, K8s, CI/CD, monitoramento (Prometheus, Grafana), logs centralizados (ELK).

## 4. Fluxo de Dados
1. Usuário realiza login e acessa a plataforma.
2. Solicitações passam pelo API Gateway, que autentica e roteia para o microsserviço adequado.
3. Microsserviços interagem entre si via mensageria para tarefas assíncronas.
4. Resultados são armazenados em bancos dedicados e disponibilizados via frontend.

## 5. Regras de Negócio
- Permissões e papéis são gerenciados centralmente.
- Coletas podem ser agendadas, reexecutadas e monitoradas.
- Relatórios são gerados automaticamente e podem ser exportados.
- Notificações são enviadas conforme eventos configurados.
- Integrações externas possuem atualização automática de tokens.

## 6. Observabilidade e Segurança
- Monitoramento de métricas e logs centralizados.
- Autenticação e autorização robustas.
- Rate limiting e proteção contra abusos.

---

> Este documento é um resumo das regras de negócio extraídas do PDF original. Para detalhes completos, consulte o documento oficial.
