from uuid import uuid4

from app.schemas.namespace import WorkloadInventory
from app.schemas.recommendation import OptimizationRecommendation, WorkloadMetric


class OptimizationEngine:
    def evaluate(
        self, workloads: list[WorkloadInventory], metrics: list[WorkloadMetric]
    ) -> list[OptimizationRecommendation]:
        metric_index = {(metric.namespace, metric.workload): metric for metric in metrics}
        recommendations: list[OptimizationRecommendation] = []

        for workload in workloads:
            metric = metric_index.get((workload.namespace, workload.name))

            if workload.cpu_limit_millicores is None or workload.memory_limit_mib is None:
                recommendations.append(
                    self._recommend(
                        workload,
                        "Governance",
                        "High",
                        "Missing resource limits",
                        "Workload has requests without complete CPU and memory limits.",
                        "resource-limits-required",
                        "Define CPU and memory limits aligned to observed p95 utilization.",
                    )
                )

            if metric and workload.cpu_request_millicores:
                cpu_ratio = metric.cpu_usage_millicores_p95 / workload.cpu_request_millicores
                if cpu_ratio < 0.25 and workload.cpu_request_millicores >= 500:
                    waste = self._estimate_cpu_waste(
                        workload.cpu_request_millicores, metric.cpu_usage_millicores_p95
                    )
                    recommendations.append(
                        self._recommend(
                            workload,
                            "Rightsizing",
                            "Medium",
                            "CPU request appears oversized",
                            (
                                f"p95 CPU usage is {metric.cpu_usage_millicores_p95}m against "
                                f"a {workload.cpu_request_millicores}m request."
                            ),
                            "cpu-p95-request-ratio-below-25-percent",
                            "Lower CPU requests after validating SLO and rollout behavior.",
                            waste,
                        )
                    )

            if metric and workload.memory_request_mib:
                memory_ratio = metric.memory_usage_mib_p95 / workload.memory_request_mib
                if memory_ratio < 0.35 and workload.memory_request_mib >= 512:
                    recommendations.append(
                        self._recommend(
                            workload,
                            "Rightsizing",
                            "Low",
                            "Memory request appears oversized",
                            (
                                f"p95 memory usage is {metric.memory_usage_mib_p95}MiB against "
                                f"a {workload.memory_request_mib}MiB request."
                            ),
                            "memory-p95-request-ratio-below-35-percent",
                            "Reduce memory requests conservatively and monitor eviction signals.",
                            18.0,
                        )
                    )

            if metric and metric.replica_count_avg == 0:
                recommendations.append(
                    self._recommend(
                        workload,
                        "Cleanup",
                        "High",
                        "Idle workload has zero active replicas",
                        "Workload has no running replicas and no observed resource usage.",
                        "zero-replicas-and-zero-usage",
                        "Confirm ownership and remove the workload or namespace if obsolete.",
                        24.0,
                    )
                )

        return recommendations

    def _recommend(
        self,
        workload: WorkloadInventory,
        category: str,
        severity: str,
        title: str,
        explanation: str,
        rule: str,
        action: str,
        waste: float = 0.0,
    ) -> OptimizationRecommendation:
        return OptimizationRecommendation(
            id=str(uuid4()),
            namespace=workload.namespace,
            workload=workload.name,
            category=category,
            severity=severity,
            title=title,
            explanation=explanation,
            deterministic_rule=rule,
            estimated_monthly_waste_usd=round(waste, 2),
            action=action,
        )

    def _estimate_cpu_waste(self, requested_millicores: int, used_millicores: int) -> float:
        excess_cores = max((requested_millicores - max(used_millicores * 2, 50)) / 1000, 0)
        return excess_cores * 22.0

