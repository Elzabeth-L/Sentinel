from fastapi import APIRouter, Depends

from app.api.deps import get_current_principal, require_platform_engineer
from app.schemas.auth import AuthenticatedPrincipal
from app.schemas.cluster import ClusterOnboardRequest, ClusterSummary
from app.services.azure_client import AzureInventoryClient

router = APIRouter()


@router.get("", response_model=list[ClusterSummary])
async def list_clusters(
    principal: AuthenticatedPrincipal = Depends(get_current_principal),
) -> list[ClusterSummary]:
    return await AzureInventoryClient(principal).list_aks_clusters()


@router.post("/onboard", response_model=ClusterSummary)
async def onboard_cluster(
    payload: ClusterOnboardRequest,
    _: AuthenticatedPrincipal = Depends(require_platform_engineer),
) -> ClusterSummary:
    return ClusterSummary(
        id=payload.azure_resource_id,
        name=payload.display_name,
        resource_group=payload.resource_group,
        subscription_id=payload.subscription_id,
        location=payload.location,
        kubernetes_version=payload.kubernetes_version,
        node_count=payload.node_count,
        onboarding_state="Onboarded",
    )

