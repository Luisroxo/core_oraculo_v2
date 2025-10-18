

from fastapi import FastAPI, Request
from auth import app as auth_app
from routes_v1 import router as v1_router
from rate_limit import limiter
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
from prometheus_fastapi_instrumentator import Instrumentator
import logging
from pythonjsonlogger import jsonlogger



# Configuração de logging estruturado (JSON) para ELK
logger = logging.getLogger()
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger.handlers = [logHandler]
logger.setLevel(logging.INFO)

app = FastAPI()
limiter.init_app(app)


# Handler para rate limit excedido
@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
	logger.warning({"event": "rate_limit_exceeded", "client": request.client.host})
	return JSONResponse(status_code=429, content={"detail": "Rate limit exceeded"})


# Rotas de autenticação (raiz)
app.mount("/", auth_app)

# Rotas versionadas (exemplo: /v1/health, /v1/info)
app.include_router(v1_router)

# Prometheus metrics endpoint
Instrumentator().instrument(app).expose(app, endpoint="/metrics", include_in_schema=False)

# Logging de requisições e respostas
@app.middleware("http")
async def log_requests(request: Request, call_next):
	logger.info({"event": "request", "method": request.method, "url": str(request.url), "client": request.client.host})
	response = await call_next(request)
	logger.info({"event": "response", "status_code": response.status_code, "url": str(request.url), "client": request.client.host})
	return response
