# Project Brain: Sentinel Resource Lifecycle Governance Platform

## Project Context

This repository implements Sentinel, an enterprise-grade Azure-native resource lifecycle governance and optimization platform. AKS governance is the first deep integration, but the product must not be treated as AKS-only. Sentinel should govern the lifecycle, ownership, hygiene, efficiency, and cleanup readiness of Azure resources as a whole, using Azure Resource Graph, Azure APIs, Kubernetes APIs, Prometheus, and Azure Monitor signals.

The user specifically requested production-oriented architecture, clean modular code, strong UI/UX, Microsoft Entra ID authentication, deterministic explainable recommendations, demo simulation support, Terraform, Helm, Docker, Kubernetes manifests, CI/CD, testing, documentation, and a maintainable handoff file. This file is the handoff source of truth for future sessions.

## Current Implementation Status

Implemented in this increment:

- Empty workspace scaffolded into a full monorepo.
- FastAPI backend foundation under `backend/`.
- Microsoft Entra ID JWT validation structure using JWKS and FastAPI dependencies.
- RBAC roles: Admin, Platform Engineer, Viewer.
- Demo-mode bearer token support using `demo-token`.
- API routes for auth, health, clusters, governance reports, and recommendations.
- SQLAlchemy models for users, clusters, namespaces, recommendations, and audit events.
- Deterministic governance engine for namespace lifecycle issues.
- Deterministic optimization engine for rightsizing and cleanup recommendations.
- Seeded demo data for stale namespaces, preview environments, idle workloads, and inefficient requests.
- Next.js App Router frontend under `frontend/`.
- Tailwind-based enterprise dashboard shell with dark/light theme support.
- React Query data access and Zustand auth state.
- MSAL client module and login/callback pages for future real Entra flow.
- Dashboard, clusters, governance, and recommendations screens.
- Backend-served preview console at `/console` for restricted laptops where Node.js/npm are unavailable. It renders friendly governance and recommendation cards using the same API data.
- `frontend/.env.local` has been created in demo mode so the local frontend does not accidentally attempt real MSAL login with placeholder values.
- Dockerfiles for backend and frontend.
- Helm chart for AKS deployment mode.
- Terraform foundation with modules for network, AKS, ACR, Key Vault, Log Analytics, Azure Monitor workspace, Managed Grafana, and Container Apps environment.
- Hosting-only Terraform for Phase 1 public VM deployment added under `terraform/vm-hosting`. This creates only app runtime hosting infrastructure and intentionally does not create AKS, databases, Container Apps, App Service, monitoring stacks, or Kubernetes resources.
- Kubernetes demo namespace manifest.
- GitHub Actions CI for backend, frontend, Terraform, and Helm.
- Documentation in `docs/`.

## Folder Structure

```text
backend/
  app/
    api/              FastAPI routers and dependencies
    core/             config, logging, auth, RBAC
    db/               SQLAlchemy base/session
    models/           persistence models
    schemas/          Pydantic API contracts
    services/         Azure/Kubernetes/Prometheus clients and rule engines
  tests/              pytest tests
frontend/
  app/                Next.js App Router pages
  components/         shell, dashboard, and UI components
  lib/                API client, auth, queries, store, types
  tests/              Playwright tests
infra/terraform/
  environments/dev/   environment composition
  modules/            reusable Azure modules
terraform/vm-hosting/
  environments/dev/   VM hosting environment composition
  modules/            network, public_ip, security, vm
  scripts/            Ubuntu bootstrap script
helm/aks-governance/  AKS deployment chart
k8s/                  demo Kubernetes resources
docs/                 architecture, API, deployment, diagrams
```

## Architecture Decisions

- Use a modular monorepo because Phase 1 is a cohesive platform and does not require microservices.
- Keep deterministic governance and optimization engines isolated from API and Azure clients. This prepares future AI support without polluting rule-based decisions.
- Use demo mode as a first-class runtime mode rather than hardcoded UI data. Backend APIs still return realistic contracts.
- Use two Microsoft Entra app registrations: one SPA app for frontend sign-in and one backend API app for scopes/audience.
- Use Microsoft Entra ID app roles for authorization. Backend role checks are required even if frontend hides navigation items.
- Use service-side Azure credentials for Azure operations. Locally this is `DefaultAzureCredential`; in AKS mode this should be Azure Workload Identity / managed identity rather than forwarded user tokens.
- Use Terraform modules from the start so Sentinel hosting, AKS target infrastructure, and future broader Azure resource governance can evolve independently.
- Phase 1 presentation hosting uses a VM-first runtime because the user needs professional public URLs immediately, with DNS and SSL, while delaying Container Apps/App Service and AI Foundry to Phase 2.
- The VM hosting Terraform is intentionally separated under `terraform/vm-hosting` and must not provision AKS clusters or governed target resources. AKS and other governed Azure resource infrastructure will live in separate future repositories.

## Product Scope Correction

Sentinel is not just an AKS cluster governance product. The Phase 1 implementation currently goes deepest on AKS because namespaces, workloads, quotas, and utilization provide a strong demo surface. The architectural direction is broader:

- Azure resource lifecycle governance across subscriptions/resource groups.
- Ownership and tagging hygiene for Azure resources.
- Stale, orphaned, idle, or unmanaged resource detection.
- Cleanup candidate analysis and approval workflows.
- AKS namespace/workload governance as one resource-family adapter.
- Future adapters for compute, networking, storage, databases, container registries, and other Azure services.

When extending the codebase, avoid naming new generic concepts as if they only belong to AKS. Prefer `resources`, `inventory`, `governance`, `lifecycle`, and `optimization` abstractions, with AKS-specific code isolated behind AKS adapters.

## Technology Stack Decisions

- Next.js App Router provides the frontend application shell and route organization.
- React Query handles API caching/loading states.
- Zustand stores client auth/session hints and role state.
- Tailwind CSS enables consistent enterprise styling without heavy UI runtime cost.
- Recharts covers phase-one charts.
- FastAPI provides typed APIs and simple dependency-based authorization.
- SQLAlchemy is used for persistence models.
- PostgreSQL is the system of record.
- Redis is reserved for cache/session/rate-limit workloads.
- Prometheus metrics are exposed with `prometheus-client`.

## Authentication Flow

Current behavior:

- In demo mode, frontend initializes with `demo-token`.
- Backend accepts `Authorization: Bearer demo-token` only when `DEMO_MODE=true`.
- Demo principal is Admin for local evaluation.

Real Entra flow intended behavior:

1. Frontend redirects through MSAL authorization code flow.
2. Entra returns an access token for the backend API app scope `api://<BACKEND_APP_CLIENT_ID>/access_as_user`.
3. Frontend sends the token to FastAPI.
4. Backend validates signature using Entra JWKS, checks issuer, audience, expiry, tenant allow-list, roles, and scopes.
5. Backend dependencies enforce Admin or Platform Engineer access where required.
6. Backend uses `DefaultAzureCredential` or managed identity for Azure Resource Graph, Azure resource discovery, AKS, and Azure Monitor operations.

Important next hardening task:

- Add a backend token exchange/session endpoint if the product should use httpOnly cookies instead of browser-held bearer tokens.
- Add refresh handling and MSAL account persistence policy.
- Configure Entra app roles exactly matching `Admin`, `Platform Engineer`, and `Viewer`.

## Backend API Summary

- `GET /api/v1/healthz`
- `GET /api/v1/readyz`
- `GET /metrics`
- `GET /api/v1/auth/me`
- `GET /api/v1/auth/openid-configuration`
- `GET /api/v1/clusters`
- `POST /api/v1/clusters/onboard`
- `GET /api/v1/governance/clusters/{cluster_id}/namespaces`
- `GET /api/v1/recommendations/clusters/{cluster_id}`

## Deterministic Rules

Governance rules:

- `missing-owner`: namespace lacks owner metadata.
- `ttl-expired`: namespace age exceeds configured TTL.
- `missing-activity-signal`: no last activity timestamp exists.
- `inactive-namespace`: last activity is older than 72 hours for non-shared namespaces.
- `scaled-to-zero-or-broken-workloads`: deployments exist but pods are absent.

Optimization rules:

- `resource-limits-required`: workload lacks CPU or memory limits.
- `cpu-p95-request-ratio-below-25-percent`: observed p95 CPU is below 25 percent of requested CPU.
- `memory-p95-request-ratio-below-35-percent`: observed p95 memory is below 35 percent of requested memory.
- `zero-replicas-and-zero-usage`: workload has no replicas and no observed usage.

Do not add fake AI recommendations. Future AI should summarize or augment rule outputs, not invent untraceable findings.

## Terraform Structure

There are now two Terraform areas with different purposes:

1. `terraform/vm-hosting`: Phase 1 app runtime hosting only.
2. `infra/terraform`: earlier broader Azure foundations. Do not extend this for the VM-first hosting request unless the user explicitly asks.

## VM Hosting Terraform Structure

Environment:

- `terraform/vm-hosting/environments/dev`

Modules:

- `network`: VNet and application subnet.
- `public_ip`: static Standard public IP for DNS A records.
- `security`: NSG with inbound SSH, HTTP, and HTTPS rules.
- `vm`: Ubuntu 22.04 LTS `Standard_B2s` VM, NIC, managed OS disk, SSH key authentication, optional system-assigned managed identity, and bootstrap custom data.

Bootstrap:

- `terraform/vm-hosting/scripts/bootstrap.sh` installs Docker, Docker Compose plugin, Nginx, Certbot, Python 3, Node.js LTS, Azure CLI, Git, jq, and prepares `/opt/aks-governance`.

DNS strategy:

- `sentinel.vaultrix.in` is an A record pointing to the VM public IP and reverse proxies to the Next.js frontend.
- API traffic should prefer same-host path routing: `https://sentinel.vaultrix.in/api/v1`.
- `api.sentinel.vaultrix.in` can remain as a compatibility alias, but it is not required.

SSL strategy:

- Nginx listens on ports 80/443.
- Let's Encrypt certificates are issued with Certbot after DNS propagation.
- Certbot configures HTTPS redirection and renewal through the system timer.
- Microsoft Entra redirect URI should be `https://sentinel.vaultrix.in/auth/callback` once SSL is active.

Managed identity strategy:

- The VM can have a system-assigned managed identity enabled by Terraform.
- Assign Azure RBAC roles to that identity for real Azure resource and AKS discovery. Minimum Phase 1 roles are Reader, Azure Kubernetes Service Cluster User Role, and Monitoring Reader. Scope roles narrowly where possible.
- This is cleaner than storing Azure credentials on the VM and aligns with the backend `DefaultAzureCredential` path.

Future migration:

- Phase 2 can move runtime hosting to Azure Container Apps, App Service, or AKS without changing the public product URLs if DNS is later pointed to the new ingress/Front Door target.

## Earlier Terraform Structure

Environment:

- `infra/terraform/environments/dev`

Modules:

- `network`: VNet and AKS subnet.
- `acr`: Azure Container Registry.
- `aks`: AKS with OIDC issuer, workload identity, Azure Policy, OMS agent, and monitor metrics.
- `key-vault`: RBAC-enabled Key Vault with purge protection.
- `observability`: Log Analytics, Azure Monitor workspace, Managed Grafana.
- `container-apps`: Container Apps managed environment foundation.

Next Terraform tasks:

- Add PostgreSQL Flexible Server or Azure Database for PostgreSQL.
- Add Azure Cache for Redis.
- Add federated identity credentials for AKS workload identity.
- Add role assignments for Resource Graph Reader, AKS Cluster User/Reader, Monitoring Reader, and Key Vault Secrets User.
- Add Container Apps resources for frontend/backend mode B.
- Add private endpoints and network restrictions for production environments.

## Deployment Architecture

Mode A: AKS

- Images are built and pushed to ACR.
- Helm deploys frontend and backend into AKS.
- Backend uses workload identity to call Azure APIs.
- Secrets should come from Key Vault through a secrets operator or CSI driver.
- Azure Monitor and Managed Prometheus collect platform telemetry.

Mode B: Azure Container Apps

- Container Apps environment module exists.
- App resources and Key Vault references are pending.
- This mode is recommended for demos or teams that do not want to host the platform in AKS.

Phase 1 VM Hosting Mode:

- Terraform under `terraform/vm-hosting` creates a public Ubuntu VM, static IP, NSG, VNet/subnet, and optional managed identity.
- Nginx terminates SSL and reverse proxies:
  - `sentinel.vaultrix.in` to frontend on `127.0.0.1:3000`
  - `sentinel.vaultrix.in/api/` to backend on `127.0.0.1:8000`
  - optional microservice paths to ports `8101` through `8104`
- This mode exists only to host the application platform for the pitch/presentation. It does not create or manage target Azure resources or AKS environments.

## Environment Variables

Important backend variables:

- `DATABASE_URL`
- `REDIS_URL`
- `BACKEND_CORS_ORIGINS`
- `SESSION_SECRET`
- `DEMO_MODE`
- `AUTO_CREATE_SCHEMA`
- `AZURE_TENANT_ID`
- `AZURE_CLIENT_ID`
- `AZURE_CLIENT_SECRET`
- `AZURE_AUTHORITY`
- `AZURE_API_AUDIENCE`
- `AZURE_ALLOWED_TENANTS`

Important frontend variables:

- `NEXT_PUBLIC_API_BASE_URL`
- `NEXT_PUBLIC_AZURE_TENANT_ID`
- `NEXT_PUBLIC_AZURE_CLIENT_ID`
- `NEXT_PUBLIC_AZURE_API_SCOPE`
- `NEXT_PUBLIC_AZURE_REDIRECT_URI`
- `NEXT_PUBLIC_DEMO_MODE`

Preferred Phase 1 frontend API value:

- `NEXT_PUBLIC_API_BASE_URL=/api/v1`

## Microservice Direction

The repo now contains a four-service split under `services/`:

- `identity-service`: token validation and principal context, port `8101`.
- `inventory-service`: Azure resource and AKS inventory, port `8102`.
- `governance-service`: lifecycle governance, port `8103`.
- `optimization-service`: resource efficiency recommendations, port `8104`.

The existing `backend/` app remains the public API gateway/BFF while these services are extracted. This keeps the VM deployment stable and gives the pitch a clear microservice architecture.

Never hardcode secrets. `.env.example` is the only env file intended for source control.

## Testing Status

Implemented:

- Backend health API test.
- Backend optimization engine unit test.
- Playwright smoke test scaffold.
- CI workflow running backend tests, frontend build, Terraform validation, and Helm lint.

Pending:

- Integration tests for auth middleware.
- Mocked Azure Resource Graph and Azure resource inventory tests.
- Mocked Kubernetes API tests.
- Frontend component tests for tables, navigation, and loading states.
- API contract tests for governance and recommendation payloads.

## Known Gaps

- Broad Azure Resource Graph inventory beyond AKS is still a hook/future adapter area.
- Real AKS discovery through `ContainerServiceClient` is implemented in `AzureInventoryClient`.
- Real Kubernetes API inventory through AKS user credentials and the Kubernetes Python client is implemented in `KubernetesInventoryClient`.
- Real Azure Managed Prometheus queries are still a hook in `WorkloadMetricsClient`.
- Database migrations are not yet set up with Alembic.
- Frontend uses in-memory bearer state; production should move to a hardened session/token refresh model.
- Container Apps mode is an infrastructure foundation only, not a full app deployment yet.
- shadcn/ui conventions are configured through `frontend/components.json`, with initial local UI primitives under `frontend/components/ui/`. More formal generated components can be added as the UI expands.
- Next.js middleware is currently non-enforcing because client-side MSAL state is not visible to middleware.

## Roadmap

Next increment:

1. Add Alembic migrations.
2. Persist onboarded clusters and namespace reports.
3. Add a generic Azure resource inventory API backed by Azure Resource Graph.
4. Harden real AKS discovery error handling and subscription filtering.
5. Add Kubernetes RBAC diagnostics for denied namespace/workload reads.
6. Implement Managed Prometheus query adapter.
7. Harden auth with backend session exchange and refresh strategy.
8. Add PostgreSQL and Redis Terraform modules.
9. Add Container Apps frontend/backend resources.
10. Add mocked Azure/Kubernetes integration tests.

Later increments:

- Namespace policy templates.
- Azure resource lifecycle policy templates.
- Cleanup approval workflow.
- Audit event viewer.
- Resource group and subscription hygiene dashboards.
- Tagging/ownership compliance for non-AKS resources.
- Cost model calibration using Azure retail prices or Cost Management exports.
- Managed Grafana dashboard provisioning.
- Multi-tenant tenant isolation model.
- Future Azure OpenAI summarization and predictive optimization, only after deterministic data quality is strong.

## Troubleshooting

- If backend startup fails on PostgreSQL, run `docker compose up -d` from the repo root.
- Schema creation is explicit. Use Alembic after the migration layer is added; `AUTO_CREATE_SCHEMA=true` is only a temporary local escape hatch.
- If auth fails locally, ensure `DEMO_MODE=true` and `NEXT_PUBLIC_DEMO_MODE=true`.
- If frontend API calls fail in Phase 1, confirm `NEXT_PUBLIC_API_BASE_URL=https://api.sentinel.vaultrix.in/api/v1` was set before the frontend build and that Nginx proxies `api.sentinel.vaultrix.in` to backend port `8000`.
- If Node.js is unavailable on the company laptop, use the VM-hosted frontend at `https://sentinel.vaultrix.in` instead of relying on local browser testing.
- If the frontend shows MSAL `interaction_in_progress`, use the login page **Reset sign-in state** button, then restart the frontend after confirming `frontend/.env.local`.
- If Terraform validation fails due provider downloads, run `terraform init` with network access.
- For Phase 1 VM hosting, use `terraform/vm-hosting/README.md`. After apply, create GoDaddy A records for `sentinel` and `api.sentinel` pointing to the VM public IP, then run Certbot on the VM.
- On May 25, 2026, `Standard_B2s` was unavailable/restricted in Central India for the active subscription. The live dev VM tfvars was changed to `Standard_L2as_v4` to continue provisioning.
- If Helm lint complains about empty secrets, pass non-empty values or use a development override file.

## Assumptions

- The first target environment is Azure commercial cloud.
- Users are in one or more Microsoft Entra tenants.
- The platform should remain a modular monolith until scale or ownership requires service separation.
- Demo support is required for limited Azure credit scenarios, but demo behavior must be isolated and explicit.
- Recommendations must remain explainable and rule-backed in Phase 1.
