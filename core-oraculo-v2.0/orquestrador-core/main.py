from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
import logging
from pythonjsonlogger import jsonlogger

app = FastAPI(title="Orquestrador Core ORÁCULO")
Instrumentator().instrument(app).expose(app, endpoint="/metrics", include_in_schema=False)

# Logging estruturado para ELK
logger = logging.getLogger()
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger.handlers = [logHandler]
logger.setLevel(logging.INFO)

@app.get("/")
def health():
    logger.info({"event": "health_check", "status": "ok"})
    return {"status": "ok", "service": "orquestrador-core"}
