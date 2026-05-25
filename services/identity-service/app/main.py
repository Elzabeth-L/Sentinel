from fastapi import Depends, FastAPI
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from backend.app.core.security import get_token_validator
from backend.app.schemas.auth import AuthenticatedPrincipal

app = FastAPI(
    title="Sentinel Identity Service",
    version="0.1.0",
    description="Authentication and principal validation service for Sentinel.",
)

bearer = HTTPBearer(auto_error=True)


@app.get("/healthz")
async def healthz() -> dict[str, str]:
    return {"status": "ok", "service": "identity"}


@app.get("/auth/me", response_model=AuthenticatedPrincipal)
async def me(credentials: HTTPAuthorizationCredentials = Depends(bearer)) -> AuthenticatedPrincipal:
    return get_token_validator().validate(credentials.credentials)
