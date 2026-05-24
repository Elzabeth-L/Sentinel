# Microsoft Entra Login Setup For Sentinel

The enterprise architecture uses **two** Microsoft Entra app registrations:

- Frontend SPA app: signs the user in.
- Backend API app: protects FastAPI and exposes API scopes.

The frontend requests an access token for the backend API. The backend validates that token. Azure resource discovery and AKS operations are performed by the backend using `DefaultAzureCredential`, which maps cleanly to managed identity on the VM.

## App Registration 1: Frontend SPA

Create an app registration:

```text
Name: Sentinel Frontend
Supported account types: Accounts in this organizational directory only
Platform: Single-page application
Redirect URI: https://sentinel.vaultrix.in/auth/callback
```

Copy:

```text
FRONTEND_APP_CLIENT_ID
TENANT_ID
```

Do not create a client secret for the SPA.

## App Registration 2: Backend API

Create another app registration:

```text
Name: Sentinel Backend API
Supported account types: Accounts in this organizational directory only
```

Copy:

```text
BACKEND_APP_CLIENT_ID
TENANT_ID
```

Open **Expose an API** and set:

```text
Application ID URI: api://<BACKEND_APP_CLIENT_ID>
```

Add a delegated scope:

```text
Scope name: access_as_user
Who can consent: Admins and users
Admin consent display name: Access Sentinel
Admin consent description: Allows the frontend to call the Sentinel backend as the signed-in user.
User consent display name: Access Sentinel
User consent description: Allows the app to call the Sentinel backend as you.
State: Enabled
```

The frontend scope is:

```text
api://<BACKEND_APP_CLIENT_ID>/access_as_user
```

## Authorize The Frontend To Call The Backend API

In the **Frontend SPA** app registration:

1. Open **API permissions**.
2. Click **Add a permission**.
3. Select **My APIs**.
4. Select `Sentinel Backend API`.
5. Select delegated permission `access_as_user`.
6. Add permissions.
7. If your tenant requires it, ask an admin to grant consent.

## Frontend Configuration

Edit `frontend/.env.local`:

```env
NEXT_PUBLIC_DEMO_MODE=false
NEXT_PUBLIC_API_BASE_URL=https://api.sentinel.vaultrix.in/api/v1
NEXT_PUBLIC_AZURE_TENANT_ID=<TENANT_ID>
NEXT_PUBLIC_AZURE_CLIENT_ID=<FRONTEND_APP_CLIENT_ID>
NEXT_PUBLIC_AZURE_API_SCOPE=api://<BACKEND_APP_CLIENT_ID>/access_as_user
NEXT_PUBLIC_AZURE_REDIRECT_URI=https://sentinel.vaultrix.in/auth/callback
```

Rebuild and restart the frontend after editing this file.

## Backend Configuration

Create or edit `backend/.env`:

```env
DEMO_MODE=false
AZURE_TENANT_ID=<TENANT_ID>
AZURE_CLIENT_ID=<BACKEND_APP_CLIENT_ID>
AZURE_API_AUDIENCE=api://<BACKEND_APP_CLIENT_ID>
AZURE_ALLOWED_TENANTS=<TENANT_ID>
AZURE_OPERATION_AUTH_MODE=default_credential
AZURE_SUBSCRIPTION_IDS=<OPTIONAL_COMMA_SEPARATED_SUBSCRIPTION_IDS>
BACKEND_CORS_ORIGINS=["https://sentinel.vaultrix.in","http://sentinel.vaultrix.in"]
```

Restart Uvicorn after editing this file.

## Azure Permissions For Real AKS Discovery

Assign these Azure RBAC roles to the identity used by the backend Azure credential.

For the Phase 1 VM, assign these roles to the VM managed identity. For developer testing, the same roles can be assigned to your signed-in Azure CLI account:

```text
Reader
Azure Kubernetes Service Cluster User Role
Monitoring Reader
```

For production, assign those roles to the backend managed identity instead.

## Local Azure Credential

`DefaultAzureCredential` tries several credential sources. For local development, the most common path is Azure CLI:

```powershell
az login
az account set --subscription <SUBSCRIPTION_ID>
```

If Azure CLI is not available on your company laptop, real AKS discovery may not work locally. Entra login can still be tested, and the production path should use managed identity.

## Testing Order

1. Test frontend Entra login.
2. Test `GET /api/v1/auth/me`.
3. Test `GET /api/v1/clusters`.
4. Select a discovered cluster.
5. Test namespace and recommendation APIs.

## If Browser Login Gets Stuck

Use one of these:

- Click **Reset sign-in state** on the login page.
- Open `https://login.microsoftonline.com/logout.srf`.
- Use an incognito browser window.
