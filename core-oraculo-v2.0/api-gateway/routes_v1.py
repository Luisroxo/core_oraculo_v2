from fastapi import APIRouter

router = APIRouter(prefix="/v1", tags=["v1"])

@router.get("/health")
def health_check():
    return {"status": "ok", "version": "v1"}

@router.get("/info")
def info():
    return {"service": "API Gateway", "version": "v1"}
