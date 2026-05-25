# Sentinel

Enterprise-grade Azure-native cloud resource lifecycle governance and optimization intelligence platform. AKS governance is the first deep integration, but the product direction covers the lifecycle, hygiene, ownership, and efficiency of Azure resources as a whole.

This repository is structured as a production-oriented full-stack platform, not a toy dashboard. The current implementation includes the first end-to-end increment: FastAPI foundation, Microsoft Entra-ready auth boundaries, deterministic governance and optimization engines, Next.js App Router shell, demo simulation data, Docker, Helm, Terraform foundations, CI, and engineering documentation.

## Stack

- Frontend: Next.js App Router, TypeScript, Tailwind CSS, React Query, Zustand, Framer Motion, Recharts
- Backend: FastAPI, SQLAlchemy, Pydantic, PostgreSQL, Redis
- Cloud: Azure, Azure Resource Graph, AKS, Azure Monitor, Managed Prometheus, ACR, Key Vault, Managed Grafana
- Infrastructure: Terraform, Docker, Kubernetes, Helm
- Observability: Prometheus metrics endpoint, structured JSON logging, health probes

## Phase 1 VM Deployment

The Phase 1 presentation runtime uses:

```text
https://sentinel.vaultrix.in
```

Use the VM hosting Terraform and deployment guide in [terraform/vm-hosting/README.md](./terraform/vm-hosting/README.md).

Frontend environment:

```env
NEXT_PUBLIC_DEMO_MODE=true
NEXT_PUBLIC_API_BASE_URL=/api/v1
NEXT_PUBLIC_AZURE_REDIRECT_URI=https://sentinel.vaultrix.in/auth/callback
```

Backend environment:

```env
DEMO_MODE=true
BACKEND_CORS_ORIGINS=["https://sentinel.vaultrix.in","http://sentinel.vaultrix.in"]
```

## Local Development Fallback

Local development remains available for engineering work, but it is not the Phase 1 presentation path.

1. Copy environment values:

```powershell
Copy-Item .env.example .env
```

2. Start dependencies:

```powershell
docker compose up -d
```

3. Run backend:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install ".[dev]"
uvicorn app.main:app --reload
```

4. Run frontend:

```powershell
cd frontend
npm install
npm run dev
```

5. For the presentation path, build and run this on the VM behind Nginx, then open `https://sentinel.vaultrix.in`.

Demo mode uses `demo-token` and seeded AKS governance data. Disable `DEMO_MODE` and `NEXT_PUBLIC_DEMO_MODE` when wiring real Microsoft Entra ID and Azure integrations.

If Node.js is not available on a restricted laptop, use the VM-hosted Sentinel URL instead of trying to run the frontend locally:

```text
https://sentinel.vaultrix.in
```

For Microsoft Entra setup, see [docs/entra-local-login.md](./docs/entra-local-login.md).

## Important Files

- [your-brain.md](./your-brain.md): complete handoff context for future coding sessions
- [backend/app/services/optimization_engine.py](./backend/app/services/optimization_engine.py): deterministic recommendation rules
- [backend/app/services/governance_engine.py](./backend/app/services/governance_engine.py): namespace lifecycle rules
- [frontend/app/page.tsx](./frontend/app/page.tsx): dashboard shell
- [terraform/vm-hosting/README.md](./terraform/vm-hosting/README.md): Phase 1 public VM hosting guide
- [docs/microservices.md](./docs/microservices.md): four-service backend split and single-host routing
- [docs/entra-single-app.md](./docs/entra-single-app.md): current one-app Microsoft Entra setup
- [infra/terraform/environments/dev/main.tf](./infra/terraform/environments/dev/main.tf): future Azure infrastructure composition
- [helm/aks-governance/values.yaml](./helm/aks-governance/values.yaml): AKS deployment configuration

## Current Status

This is a strong first production-grade increment. The remaining work is tracked in `your-brain.md`: full database migrations, real Azure Resource Graph queries, Kubernetes API client implementation, Managed Prometheus queries, backend token exchange/session hardening, and deeper test coverage.
