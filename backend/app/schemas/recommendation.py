from pydantic import BaseModel


class WorkloadMetric(BaseModel):
    namespace: str
    workload: str
    cpu_usage_millicores_p95: int
    memory_usage_mib_p95: int
    replica_count_avg: float


class OptimizationRecommendation(BaseModel):
    id: str
    namespace: str
    workload: str
    category: str
    severity: str
    title: str
    explanation: str
    deterministic_rule: str
    estimated_monthly_waste_usd: float = 0
    action: str

