from datetime import UTC, datetime, timedelta

from app.schemas.namespace import NamespaceInventory, WorkloadInventory
from app.schemas.recommendation import WorkloadMetric

now = datetime.now(UTC)

DEMO_NAMESPACES = [
    NamespaceInventory(
        name="checkout-pr-1842",
        owner="mira.chen@example.com",
        team="payments",
        environment_type="preview",
        ttl_hours=48,
        created_at=now - timedelta(hours=92),
        last_activity_at=now - timedelta(hours=70),
        services_count=2,
        pods_count=6,
        deployments_count=3,
    ),
    NamespaceInventory(
        name="catalog-dev",
        owner="samir.patel@example.com",
        team="commerce",
        environment_type="development",
        ttl_hours=168,
        created_at=now - timedelta(days=11),
        last_activity_at=now - timedelta(hours=8),
        services_count=4,
        pods_count=12,
        deployments_count=5,
    ),
    NamespaceInventory(
        name="legacy-import-test",
        owner=None,
        team="data-platform",
        environment_type="test",
        ttl_hours=72,
        created_at=now - timedelta(days=18),
        last_activity_at=now - timedelta(days=14),
        services_count=1,
        pods_count=0,
        deployments_count=2,
    ),
    NamespaceInventory(
        name="observability",
        owner="platform@example.com",
        team="platform",
        environment_type="shared",
        ttl_hours=None,
        created_at=now - timedelta(days=120),
        last_activity_at=now - timedelta(minutes=12),
        services_count=8,
        pods_count=24,
        deployments_count=9,
    ),
]

DEMO_WORKLOADS = [
    WorkloadInventory(
        namespace="checkout-pr-1842",
        name="checkout-api",
        kind="Deployment",
        replicas=3,
        cpu_request_millicores=1500,
        memory_request_mib=2048,
        cpu_limit_millicores=None,
        memory_limit_mib=None,
        last_rollout_at=now - timedelta(days=5),
    ),
    WorkloadInventory(
        namespace="catalog-dev",
        name="catalog-worker",
        kind="Deployment",
        replicas=2,
        cpu_request_millicores=1000,
        memory_request_mib=1024,
        cpu_limit_millicores=2000,
        memory_limit_mib=2048,
        last_rollout_at=now - timedelta(days=12),
    ),
    WorkloadInventory(
        namespace="legacy-import-test",
        name="import-job-runner",
        kind="Deployment",
        replicas=0,
        cpu_request_millicores=500,
        memory_request_mib=512,
        cpu_limit_millicores=None,
        memory_limit_mib=None,
        last_rollout_at=now - timedelta(days=18),
    ),
]

DEMO_METRICS = [
    WorkloadMetric(
        namespace="checkout-pr-1842",
        workload="checkout-api",
        cpu_usage_millicores_p95=110,
        memory_usage_mib_p95=220,
        replica_count_avg=3,
    ),
    WorkloadMetric(
        namespace="catalog-dev",
        workload="catalog-worker",
        cpu_usage_millicores_p95=420,
        memory_usage_mib_p95=650,
        replica_count_avg=2,
    ),
    WorkloadMetric(
        namespace="legacy-import-test",
        workload="import-job-runner",
        cpu_usage_millicores_p95=0,
        memory_usage_mib_p95=0,
        replica_count_avg=0,
    ),
]

