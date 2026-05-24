from datetime import UTC, datetime

from app.schemas.namespace import NamespaceGovernanceReport, NamespaceInventory


class GovernanceEngine:
    def evaluate_namespaces(
        self, namespaces: list[NamespaceInventory]
    ) -> list[NamespaceGovernanceReport]:
        now = datetime.now(UTC)
        reports: list[NamespaceGovernanceReport] = []

        for namespace in namespaces:
            age_hours = int((now - namespace.created_at).total_seconds() // 3600)
            last_activity_hours = (
                int((now - namespace.last_activity_at).total_seconds() // 3600)
                if namespace.last_activity_at
                else None
            )
            violations: list[str] = []

            if not namespace.owner:
                violations.append("missing-owner")
            if namespace.ttl_hours is not None and age_hours > namespace.ttl_hours:
                violations.append("ttl-expired")
            if last_activity_hours is None:
                violations.append("missing-activity-signal")
            elif last_activity_hours > 72 and namespace.environment_type != "shared":
                violations.append("inactive-namespace")
            if namespace.pods_count == 0 and namespace.deployments_count > 0:
                violations.append("scaled-to-zero-or-broken-workloads")

            cleanup_candidate = "ttl-expired" in violations or "inactive-namespace" in violations
            score = max(0, 100 - (len(violations) * 18) - (20 if cleanup_candidate else 0))
            status = "Healthy"
            if cleanup_candidate:
                status = "Cleanup Candidate"
            elif violations:
                status = "Needs Attention"

            reports.append(
                NamespaceGovernanceReport(
                    namespace=namespace.name,
                    owner=namespace.owner,
                    team=namespace.team,
                    environment_type=namespace.environment_type,
                    age_hours=age_hours,
                    ttl_hours=namespace.ttl_hours,
                    last_activity_hours=last_activity_hours,
                    status=status,
                    violations=violations,
                    cleanup_candidate=cleanup_candidate,
                    efficiency_score=score,
                )
            )

        return sorted(reports, key=lambda item: (not item.cleanup_candidate, item.efficiency_score))

