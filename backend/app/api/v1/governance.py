from fastapi import APIRouter, Depends

from app.api.deps import get_current_principal
from app.schemas.auth import AuthenticatedPrincipal
from app.schemas.namespace import NamespaceGovernanceReport
from app.services.governance_engine import GovernanceEngine
from app.services.kubernetes_client import KubernetesInventoryClient

router = APIRouter()


@router.get("/clusters/{cluster_id}/namespaces", response_model=list[NamespaceGovernanceReport])
async def namespace_governance(
    cluster_id: str,
    principal: AuthenticatedPrincipal = Depends(get_current_principal),
) -> list[NamespaceGovernanceReport]:
    inventory = await KubernetesInventoryClient(principal).list_namespaces(cluster_id)
    return GovernanceEngine().evaluate_namespaces(inventory)

