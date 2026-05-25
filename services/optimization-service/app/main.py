from fastapi import Depends, FastAPI
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from backend.app.core.security import get_token_validator
from backend.app.schemas.auth import AuthenticatedPrincipal
from backend.app.schemas.recommendation import OptimizationRecommendation
from backend.app.services.kubernetes_client import KubernetesInventoryClient
from backend.app.services.optimization_engine import OptimizationEngine
from backend.app.services.prometheus_client import WorkloadMetricsClient

app = FastAPI(
    title="Sentinel Optimization Service",
    version="0.1.0",
    description="Resource efficiency and deterministic recommendation service for Sentinel.",
)

bearer = HTTPBearer(auto_error=True)


def current_principal(
    credentials: HTTPAuthorizationCredentials = Depends(bearer),
) -> AuthenticatedPrincipal:
    return get_token_validator().validate(credentials.credentials)


@app.get("/healthz")
async def healthz() -> dict[str, str]:
    return {"status": "ok", "service": "optimization"}


@app.get("/clusters/{cluster_id}", response_model=list[OptimizationRecommendation])
async def recommendations(
    cluster_id: str,
    principal: AuthenticatedPrincipal = Depends(current_principal),
) -> list[OptimizationRecommendation]:
    inventory = await KubernetesInventoryClient(principal).list_workloads(cluster_id)
    metrics = await WorkloadMetricsClient(principal).workload_metrics(cluster_id)
    return OptimizationEngine().evaluate(inventory, metrics)
