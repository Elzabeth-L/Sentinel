from fastapi import APIRouter

from app.schemas.common import HealthResponse

router = APIRouter()


@router.get("/healthz", response_model=HealthResponse)
def healthz() -> HealthResponse:
    return HealthResponse(status="ok")


@router.get("/readyz", response_model=HealthResponse)
def readyz() -> HealthResponse:
    return HealthResponse(status="ready")

