from fastapi import Depends, FastAPI
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from backend.app.core.security import get_token_validator
from backend.app.schemas.auth import AuthenticatedPrincipal
from backend.app.schemas.cluster import ClusterSummary
from backend.app.services.azure_client import AzureInventoryClient

app = FastAPI(
    title="Sentinel Inventory Service",
    version="0.1.0",
    description="Azure resource and AKS inventory discovery service for Sentinel.",
)

bearer = HTTPBearer(auto_error=True)


def current_principal(
    credentials: HTTPAuthorizationCredentials = Depends(bearer),
) -> AuthenticatedPrincipal:
    return get_token_validator().validate(credentials.credentials)


@app.get("/healthz")
async def healthz() -> dict[str, str]:
    return {"status": "ok", "service": "inventory"}


@app.get("/clusters", response_model=list[ClusterSummary])
async def list_clusters(
    principal: AuthenticatedPrincipal = Depends(current_principal),
) -> list[ClusterSummary]:
    return await AzureInventoryClient(principal).list_aks_clusters()
