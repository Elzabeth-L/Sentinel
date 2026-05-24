import base64
from datetime import UTC, datetime
from typing import Any

import yaml
from azure.mgmt.containerservice import ContainerServiceClient
from kubernetes import client, config

from app.core.config import settings
from app.schemas.auth import AuthenticatedPrincipal
from app.schemas.namespace import NamespaceInventory, WorkloadInventory
from app.services.azure_credentials import get_azure_operation_credential
from app.services.azure_resource_id import parse_aks_resource_id
from app.services.demo_data import DEMO_NAMESPACES, DEMO_WORKLOADS


class KubernetesInventoryClient:
    def __init__(self, principal: AuthenticatedPrincipal) -> None:
        self.principal = principal

    async def list_namespaces(self, cluster_id: str) -> list[NamespaceInventory]:
        if settings.demo_mode:
            return DEMO_NAMESPACES

        core_api, apps_api = self._build_clients(cluster_id)
        namespaces = core_api.list_namespace().items
        pods = core_api.list_pod_for_all_namespaces().items
        services = core_api.list_service_for_all_namespaces().items
        deployments = apps_api.list_deployment_for_all_namespaces().items

        pod_count = self._count_by_namespace(pods)
        service_count = self._count_by_namespace(services)
        deployment_count = self._count_by_namespace(deployments)

        return [
            NamespaceInventory(
                name=namespace.metadata.name,
                owner=self._metadata_value(namespace, "owner"),
                team=self._metadata_value(namespace, "team"),
                environment_type=self._metadata_value(namespace, "environment-type"),
                ttl_hours=self._int_metadata_value(namespace, "ttl-hours"),
                created_at=namespace.metadata.creation_timestamp or datetime.now(UTC),
                last_activity_at=self._datetime_metadata_value(namespace, "last-activity-time"),
                services_count=service_count.get(namespace.metadata.name, 0),
                pods_count=pod_count.get(namespace.metadata.name, 0),
                deployments_count=deployment_count.get(namespace.metadata.name, 0),
            )
            for namespace in namespaces
        ]

    async def list_workloads(self, cluster_id: str) -> list[WorkloadInventory]:
        if settings.demo_mode:
            return DEMO_WORKLOADS

        _, apps_api = self._build_clients(cluster_id)
        workloads: list[WorkloadInventory] = []
        for deployment in apps_api.list_deployment_for_all_namespaces().items:
            containers = deployment.spec.template.spec.containers or []
            requests = [container.resources.requests or {} for container in containers]
            limits = [container.resources.limits or {} for container in containers]

            workloads.append(
                WorkloadInventory(
                    namespace=deployment.metadata.namespace,
                    name=deployment.metadata.name,
                    kind="Deployment",
                    replicas=deployment.spec.replicas or 0,
                    cpu_request_millicores=sum(self._cpu_to_millicores(item.get("cpu")) for item in requests),
                    memory_request_mib=sum(self._memory_to_mib(item.get("memory")) for item in requests),
                    cpu_limit_millicores=sum(self._cpu_to_millicores(item.get("cpu")) for item in limits) or None,
                    memory_limit_mib=sum(self._memory_to_mib(item.get("memory")) for item in limits) or None,
                    last_rollout_at=deployment.metadata.creation_timestamp,
                )
            )
        return workloads

    def _build_clients(self, cluster_id: str) -> tuple[client.CoreV1Api, client.AppsV1Api]:
        aks_id = parse_aks_resource_id(cluster_id)
        containers = ContainerServiceClient(get_azure_operation_credential(), aks_id.subscription_id)
        credentials = containers.managed_clusters.list_cluster_user_credentials(
            aks_id.resource_group,
            aks_id.cluster_name,
        )
        kubeconfig_dict = self._decode_kubeconfig(credentials.kubeconfigs[0].value)
        api_client = config.new_client_from_config_dict(kubeconfig_dict)
        return client.CoreV1Api(api_client), client.AppsV1Api(api_client)

    def _decode_kubeconfig(self, raw_value: bytes | str) -> dict[str, Any]:
        if isinstance(raw_value, bytes):
            text = raw_value.decode("utf-8")
        else:
            try:
                text = base64.b64decode(raw_value).decode("utf-8")
            except Exception:
                text = raw_value
        return yaml.safe_load(text)

    def _count_by_namespace(self, items: list[Any]) -> dict[str, int]:
        counts: dict[str, int] = {}
        for item in items:
            namespace = item.metadata.namespace
            counts[namespace] = counts.get(namespace, 0) + 1
        return counts

    def _metadata_value(self, item: Any, key: str) -> str | None:
        annotations = item.metadata.annotations or {}
        labels = item.metadata.labels or {}
        return annotations.get(f"governance.azure-native.io/{key}") or labels.get(
            f"governance.azure-native.io/{key}"
        )

    def _int_metadata_value(self, item: Any, key: str) -> int | None:
        value = self._metadata_value(item, key)
        return int(value) if value and value.isdigit() else None

    def _datetime_metadata_value(self, item: Any, key: str) -> datetime | None:
        value = self._metadata_value(item, key)
        if not value:
            return None
        return datetime.fromisoformat(value.replace("Z", "+00:00"))

    def _cpu_to_millicores(self, value: str | None) -> int:
        if not value:
            return 0
        if value.endswith("m"):
            return int(value[:-1])
        return int(float(value) * 1000)

    def _memory_to_mib(self, value: str | None) -> int:
        if not value:
            return 0
        normalized = value.strip()
        if normalized.endswith("Mi"):
            return int(normalized[:-2])
        if normalized.endswith("Gi"):
            return int(float(normalized[:-2]) * 1024)
        if normalized.endswith("M"):
            return int(normalized[:-1])
        if normalized.endswith("G"):
            return int(float(normalized[:-1]) * 1024)
        return int(int(normalized) / 1024 / 1024)
