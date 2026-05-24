# API Documentation

Base path: `/api/v1`

## Auth

- `GET /auth/me`: returns validated principal, roles, scopes, and tenant.
- `GET /auth/openid-configuration`: returns the configured Entra OpenID metadata.

## Health

- `GET /healthz`: liveness check.
- `GET /readyz`: readiness check.
- `GET /metrics`: Prometheus metrics endpoint mounted outside `/api/v1`.

## Clusters

- `GET /clusters`: list accessible AKS clusters. Demo mode returns seeded clusters.
- `POST /clusters/onboard`: onboard a discovered cluster. Requires Platform Engineer or Admin.

## Governance

- `GET /governance/clusters/{cluster_id}/namespaces`: returns namespace lifecycle governance reports.

Rules currently implemented:

- missing owner
- TTL expired
- missing activity signal
- inactive namespace
- scaled-to-zero or broken workloads

## Recommendations

- `GET /recommendations/clusters/{cluster_id}`: returns deterministic optimization recommendations.

Rules currently implemented:

- missing resource limits
- CPU p95/request ratio below 25 percent
- memory p95/request ratio below 35 percent
- zero replicas and zero usage

