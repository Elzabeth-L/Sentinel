# Sentinel Microservices Structure

Sentinel is moving from a modular monolith toward four deployable backend services:

| Service | Port | Responsibility |
| --- | ---: | --- |
| identity-service | 8101 | Token validation and principal context |
| inventory-service | 8102 | Azure resource and AKS inventory discovery |
| governance-service | 8103 | Lifecycle policy evaluation and stale resource detection |
| optimization-service | 8104 | Utilization analysis and deterministic recommendations |

The existing `backend/` app remains the API gateway/BFF for the current VM deployment. It keeps the public API stable while service boundaries are extracted.

## Run Services

```bash
docker compose -f docker-compose.microservices.yml up --build
```

Health checks:

```bash
curl http://127.0.0.1:8101/healthz
curl http://127.0.0.1:8102/healthz
curl http://127.0.0.1:8103/healthz
curl http://127.0.0.1:8104/healthz
```

## Single Host Routing

Use one public host:

```text
https://sentinel.vaultrix.in
```

Route by path:

```text
/              -> frontend
/api/v1/*      -> current backend gateway
/identity/*    -> identity-service
/inventory/*   -> inventory-service
/governance/*  -> governance-service
/optimization/* -> optimization-service
```

This means the frontend can use:

```env
NEXT_PUBLIC_API_BASE_URL=/api/v1
```

The two Entra app registrations are still recommended. They are not required because of subdomains; they are recommended because OAuth separates the public client app from the protected API resource.
