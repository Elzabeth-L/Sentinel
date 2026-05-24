from fastapi import APIRouter, Depends

from app.api.deps import get_current_principal
from app.schemas.auth import AuthenticatedPrincipal
from app.schemas.recommendation import OptimizationRecommendation
from app.services.kubernetes_client import KubernetesInventoryClient
from app.services.optimization_engine import OptimizationEngine
from app.services.prometheus_client import WorkloadMetricsClient

router = APIRouter()


@router.get("/clusters/{cluster_id}", response_model=list[OptimizationRecommendation])
async def recommendations(
    cluster_id: str,
    principal: AuthenticatedPrincipal = Depends(get_current_principal),
) -> list[OptimizationRecommendation]:
    inventory = await KubernetesInventoryClient(principal).list_workloads(cluster_id)
    metrics = await WorkloadMetricsClient(principal).workload_metrics(cluster_id)
    return OptimizationEngine().evaluate(inventory, metrics)

