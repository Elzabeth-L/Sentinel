# Azure-Native Kubernetes Environment Governance & Resource Optimization Platform

Enterprise-grade operational governance and optimization intelligence layer for Azure Kubernetes Service environments.

This repository is structured as a production-oriented full-stack platform, not a toy dashboard. The current implementation includes the first end-to-end increment: FastAPI foundation, Microsoft Entra-ready auth boundaries, deterministic governance and optimization engines, Next.js App Router shell, demo simulation data, Docker, Helm, Terraform foundations, CI, and engineering documentation.

## Stack

- Frontend: Next.js App Router, TypeScript, Tailwind CSS, React Query, Zustand, Framer Motion, Recharts
- Backend: FastAPI, SQLAlchemy, Pydantic, PostgreSQL, Redis
- Cloud: Azure, AKS, Azure Monitor, Managed Prometheus, Resource Graph, ACR, Key Vault, Managed Grafana
- Infrastructure: Terraform, Docker, Kubernetes, Helm
- Observability: Prometheus metrics endpoint, structured JSON logging, health probes

## Local Development

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

5. Open `http://localhost:3000`.

Demo mode uses `demo-token` and seeded AKS governance data. Disable `DEMO_MODE` and `NEXT_PUBLIC_DEMO_MODE` when wiring real Microsoft Entra ID and Azure integrations.

If Node.js is not available on a restricted laptop, you can still test a friendly backend-served preview UI after starting FastAPI:

```text
http://localhost:8000/console
```

For Microsoft Entra local login, see [docs/entra-local-login.md](./docs/entra-local-login.md).

## Important Files

- [your-brain.md](./your-brain.md): complete handoff context for future coding sessions
- [backend/app/services/optimization_engine.py](./backend/app/services/optimization_engine.py): deterministic recommendation rules
- [backend/app/services/governance_engine.py](./backend/app/services/governance_engine.py): namespace lifecycle rules
- [frontend/app/page.tsx](./frontend/app/page.tsx): dashboard shell
- [infra/terraform/environments/dev/main.tf](./infra/terraform/environments/dev/main.tf): dev infrastructure composition
- [helm/aks-governance/values.yaml](./helm/aks-governance/values.yaml): AKS deployment configuration

## Current Status

This is a strong first production-grade increment. The remaining work is tracked in `your-brain.md`: full database migrations, real Azure Resource Graph queries, Kubernetes API client implementation, Managed Prometheus queries, backend token exchange/session hardening, and deeper test coverage.
