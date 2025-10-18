# Interface com Mensageria

## Visão Geral
A interface com mensageria é responsável por garantir a comunicação assíncrona, escalável e resiliente entre o Orquestrador Core, escavadores e executadores.

## Tecnologias Suportadas
- **RabbitMQ** (AMQP)
- **Redis Streams**
- **NATS**

## Estratégia de Integração
- **Publicação de mensagens**: O orquestrador publica mensagens em filas/tópicos específicos para cada tipo de tarefa.
- **Consumo de mensagens**: Escavadores e executadores consomem mensagens das filas/tópicos designados.
- **Confirmação/Ack**: Mensagens só são removidas da fila após processamento bem-sucedido (garantia de entrega).
- **Dead Letter Queue (DLQ)**: Mensagens que falham repetidamente são redirecionadas para uma fila de quarentena.

## Padrão de Mensagem
```json
{
  "correlation_id": "uuid",
  "tipo_evento": "iniciar_coleta|resultado_coleta|iniciar_execucao|resultado_execucao",
  "payload": {...},
  "timestamp": "2025-10-14T12:00:00Z"
}
```

## Exemplo de Publicação (RabbitMQ, pika)
```python
import pika
import json

connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
channel = connection.channel()
channel.queue_declare(queue='escavador_youtube')

mensagem = {
    "correlation_id": "123e4567-e89b-12d3-a456-426614174000",
    "tipo_evento": "iniciar_coleta",
    "payload": {"param": "valor"},
    "timestamp": "2025-10-14T12:00:00Z"
}
channel.basic_publish(
    exchange='',
    routing_key='escavador_youtube',
    body=json.dumps(mensagem)
)
connection.close()
```

## Exemplo de Consumo (RabbitMQ, pika)
```python
import pika
import json

def callback(ch, method, properties, body):
    mensagem = json.loads(body)
    print(f"Recebido: {mensagem}")
    ch.basic_ack(delivery_tag=method.delivery_tag)

connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
channel = connection.channel()
channel.queue_declare(queue='escavador_youtube')
channel.basic_consume(queue='escavador_youtube', on_message_callback=callback)
channel.start_consuming()
```

## Boas Práticas
- Utilizar `correlation_id` para rastreabilidade ponta a ponta.
- Implementar DLQ para mensagens problemáticas.
- Monitorar filas e métricas de consumo.
- Configurar timeouts e retries.
- Garantir idempotência no processamento.

## Referências
- [RabbitMQ - Padrões de Mensageria](https://www.rabbitmq.com/tutorials/tutorial-one-python.html)
- [Redis Streams](https://redis.io/docs/data-types/streams/)
- [NATS - Guia de Introdução](https://docs.nats.io/nats-concepts/intro)

---

> **Próximos passos:**
> - Implementar camada de abstração para mensageria.
> - Testar publicação e consumo com diferentes brokers.
> - Integrar métricas e logs para observabilidade.
