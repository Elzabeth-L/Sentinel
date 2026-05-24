from datetime import datetime

from pydantic import BaseModel


class WorkloadInventory(BaseModel):
    namespace: str
    name: str
    kind: str
    replicas: int
    cpu_request_millicores: int | None = None
    memory_request_mib: int | None = None
    cpu_limit_millicores: int | None = None
    memory_limit_mib: int | None = None
    last_rollout_at: datetime | None = None


class NamespaceInventory(BaseModel):
    name: str
    owner: str | None = None
    team: str | None = None
    environment_type: str | None = None
    ttl_hours: int | None = None
    created_at: datetime
    last_activity_at: datetime | None = None
    services_count: int = 0
    pods_count: int = 0
    deployments_count: int = 0


class NamespaceGovernanceReport(BaseModel):
    namespace: str
    owner: str | None
    team: str | None
    environment_type: str | None
    age_hours: int
    ttl_hours: int | None
    last_activity_hours: int | None
    status: str
    violations: list[str]
    cleanup_candidate: bool
    efficiency_score: int

