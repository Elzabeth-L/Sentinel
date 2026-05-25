from azure.mgmt.containerservice import ContainerServiceClient
from azure.mgmt.resourcegraph import ResourceGraphClient
from azure.mgmt.resourcegraph.models import QueryRequest
from azure.mgmt.subscription import SubscriptionClient

from app.core.config import settings
from app.schemas.auth import AuthenticatedPrincipal
from app.schemas.cluster import ClusterSummary
from app.schemas.resource import AzureResourceSummary
from app.services.azure_credentials import get_azure_operation_credential


class AzureInventoryClient:
    def __init__(self, principal: AuthenticatedPrincipal) -> None:
        self.principal = principal

    async def list_aks_clusters(self) -> list[ClusterSummary]:
        if settings.demo_mode:
            return [
                ClusterSummary(
                    id="/subscriptions/demo/resourceGroups/rg-platform/providers/Microsoft.ContainerService/managedClusters/aks-platform-prod",
                    name="aks-platform-prod",
                    subscription_id="demo",
                    resource_group="rg-platform",
                    location="eastus",
                    kubernetes_version="1.30.5",
                    node_count=6,
                    onboarding_state="Onboarded",
                ),
                ClusterSummary(
                    id="/subscriptions/demo/resourceGroups/rg-preview/providers/Microsoft.ContainerService/managedClusters/aks-preview",
                    name="aks-preview",
                    subscription_id="demo",
                    resource_group="rg-preview",
                    location="eastus2",
                    kubernetes_version="1.30.5",
                    node_count=3,
                    onboarding_state="Discovered",
                ),
            ]

        subscription_ids = settings.azure_subscription_ids or self._discover_subscription_ids()
        clusters: list[ClusterSummary] = []

        for subscription_id in subscription_ids:
            client = ContainerServiceClient(get_azure_operation_credential(), subscription_id)
            for cluster in client.managed_clusters.list():
                agent_pools = cluster.agent_pool_profiles or []
                clusters.append(
                    ClusterSummary(
                        id=cluster.id or "",
                        name=cluster.name or "",
                        subscription_id=subscription_id,
                        resource_group=self._resource_group_from_id(cluster.id or ""),
                        location=cluster.location or "",
                        kubernetes_version=cluster.kubernetes_version or "unknown",
                        node_count=sum(pool.count or 0 for pool in agent_pools),
                        onboarding_state="Discovered",
                    )
                )

        return clusters

    async def list_resources(self) -> list[AzureResourceSummary]:
        subscription_ids = settings.azure_subscription_ids or self._discover_subscription_ids()
        query = """
        Resources
        | project id, name, type, resourceGroup, subscriptionId, location, kind, tags
        | order by type asc, name asc
        """
        client = ResourceGraphClient(get_azure_operation_credential())
        response = client.resources(
            QueryRequest(
                subscriptions=subscription_ids,
                query=query,
                options={"resultFormat": "objectArray"},
            )
        )
        return [AzureResourceSummary.model_validate(item) for item in response.data or []]

    def _discover_subscription_ids(self) -> list[str]:
        client = SubscriptionClient(get_azure_operation_credential())
        return [subscription.subscription_id for subscription in client.subscriptions.list()]

    def _resource_group_from_id(self, resource_id: str) -> str:
        parts = [part for part in resource_id.strip("/").split("/") if part]
        lower = [part.lower() for part in parts]
        if "resourcegroups" not in lower:
            return ""
        return parts[lower.index("resourcegroups") + 1]
