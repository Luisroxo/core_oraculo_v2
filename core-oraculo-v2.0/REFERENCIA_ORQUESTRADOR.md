# Referência Técnica: Orquestração de Escavadores e Executadores

## Stack Oficial
- **Linguagem:** Python 3.11+
- **Framework:** FastAPI (API/admin), Celery (orquestração assíncrona)
- **Mensageria:** RabbitMQ (prioritário), Redis Streams (fallback)
- **Banco de Estado:** Redis (opcional, para locks e cache)
- **Observabilidade:** Prometheus (métricas), ELK Stack (logs estruturados)
- **Deploy:** Docker, Kubernetes

## Padrão de Mensagens
- **Formato:** JSON
- **Campos obrigatórios:**
  - `correlation_id`: string (rastreamento)
  - `tipo_evento`: string (ex: "iniciar_coleta", "resultado_coleta", "iniciar_execucao", "resultado_execucao")
  - `payload`: objeto (dados do evento)
  - `timestamp`: ISO8601
- **Exemplo:**
```json
{
  "correlation_id": "abc123",
  "tipo_evento": "iniciar_coleta",
  "payload": {"fonte": "youtube", "parametros": {...}},
  "timestamp": "2025-10-14T12:00:00Z"
}
```

## Fluxo de Orquestração
1. Orquestrador recebe requisição (API ou evento).
2. Publica mensagem `iniciar_coleta` na fila do escavador correspondente.
3. Escavador executa, publica `resultado_coleta` na fila de resultados.
4. Orquestrador consome resultado, publica `iniciar_execucao` para o executador.
5. Executador processa, publica `resultado_execucao`.
6. Orquestrador agrega, armazena e notifica (via API, webhook, etc).

## Contratos de Integração
- **Escavadores:**
  - Consomem eventos `iniciar_coleta`.
  - Publicam eventos `resultado_coleta`.
- **Executadores:**
  - Consomem eventos `iniciar_execucao`.
  - Publicam eventos `resultado_execucao`.
- **Orquestrador:**
  - Publica e consome todos os eventos, mantém rastreamento por `correlation_id`.

## Estratégias
- **Escalabilidade:** múltiplos workers Celery, filas dedicadas por fonte/tipo.
- **Monitoramento:** métricas customizadas (tempo de ciclo, falhas, throughput).
- **Logs:** sempre estruturados, com correlation_id.
- **Resiliência:** retries automáticos, dead-letter queue.

## Exemplo de Código (Celery Task)
```python
from celery import Celery
app = Celery('orquestrador', broker='pyamqp://guest@rabbitmq//')

@app.task(bind=True, max_retries=3)
def iniciar_coleta(self, correlation_id, fonte, parametros):
    # Publica mensagem para escavador
    ...
```

---

Este documento deve ser revisado e expandido conforme a implementação evoluir.