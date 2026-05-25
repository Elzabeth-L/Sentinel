from fastapi import Depends, FastAPI
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from backend.app.core.security import get_token_validator
from backend.app.schemas.auth import AuthenticatedPrincipal
from backend.app.schemas.namespace import NamespaceGovernanceReport
from backend.app.services.governance_engine import GovernanceEngine
from backend.app.services.kubernetes_client import KubernetesInventoryClient

app = FastAPI(
    title="Sentinel Governance Service",
    version="0.1.0",
    description="Lifecycle governance and policy evaluation service for Sentinel.",
)

bearer = HTTPBearer(auto_error=True)


def current_principal(
    credentials: HTTPAuthorizationCredentials = Depends(bearer),
) -> AuthenticatedPrincipal:
    return get_token_validator().validate(credentials.credentials)


@app.get("/healthz")
async def healthz() -> dict[str, str]:
    return {"status": "ok", "service": "governance"}


@app.get("/clusters/{cluster_id}/namespaces", response_model=list[NamespaceGovernanceReport])
async def namespace_governance(
    cluster_id: str,
    principal: AuthenticatedPrincipal = Depends(current_principal),
) -> list[NamespaceGovernanceReport]:
    inventory = await KubernetesInventoryClient(principal).list_namespaces(cluster_id)
    return GovernanceEngine().evaluate_namespaces(inventory)
