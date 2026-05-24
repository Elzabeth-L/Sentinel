from app.core.config import settings
from app.schemas.auth import AuthenticatedPrincipal
from app.schemas.recommendation import WorkloadMetric
from app.services.demo_data import DEMO_METRICS


class WorkloadMetricsClient:
    def __init__(self, principal: AuthenticatedPrincipal) -> None:
        self.principal = principal

    async def workload_metrics(self, cluster_id: str) -> list[WorkloadMetric]:
        if settings.demo_mode:
            return DEMO_METRICS

        # Production implementation hook:
        # Query Azure Managed Prometheus using Azure Monitor workspace endpoints.
        return []

