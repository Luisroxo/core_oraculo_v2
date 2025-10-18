from celery import Celery

celery_app = Celery(
    'orquestrador_core',
    broker='pyamqp://guest@rabbitmq//',
    backend='redis://redis/0'
)

# Exemplo de task Celery
@celery_app.task(bind=True, max_retries=3)
def exemplo_task(self, correlation_id, tipo_evento, payload):
    # Lógica de orquestração
    return {"correlation_id": correlation_id, "tipo_evento": tipo_evento, "payload": payload}
