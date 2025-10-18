from slowapi import Limiter
from slowapi.util import get_remote_address
from fastapi import Request

# Limite: 5 requisições por minuto por IP
limiter = Limiter(key_func=get_remote_address, default_limits=["5/minute"])

# Exemplo de uso em rota:
# from slowapi.errors import RateLimitExceeded
# from fastapi.responses import JSONResponse
#
# @app.exception_handler(RateLimitExceeded)
# async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
#     return JSONResponse(status_code=429, content={"detail": "Rate limit exceeded"})
