from dataclasses import dataclass


@dataclass(frozen=True)
class AksResourceId:
    subscription_id: str
    resource_group: str
    cluster_name: str


def parse_aks_resource_id(resource_id: str) -> AksResourceId:
    parts = [part for part in resource_id.strip("/").split("/") if part]
    lower = [part.lower() for part in parts]

    return AksResourceId(
        subscription_id=parts[lower.index("subscriptions") + 1],
        resource_group=parts[lower.index("resourcegroups") + 1],
        cluster_name=parts[lower.index("managedclusters") + 1],
    )
