# Microsoft Entra Single App Registration Setup

Sentinel is currently configured to use one Microsoft Entra app registration:

```text
Tenant ID: 61d2b850-89ba-4674-9fc4-42d9ff6bdaa5
Application client ID: 14467cba-ecd6-4f59-a06c-b5d1b1621a93
Application name: Sentinel Vaultrix
Public URL: https://sentinel.vaultrix.in
```

This single registration is used as both:

- the SPA client that signs users in
- the protected API resource that exposes `access_as_user`

## Authentication

In the app registration, open **Authentication** and add a platform:

```text
Platform: Single-page application
Redirect URI: https://sentinel.vaultrix.in/auth/callback
```

Do not create a client secret for the SPA.

## Expose An API

Open **Expose an API**.

Set Application ID URI:

```text
api://14467cba-ecd6-4f59-a06c-b5d1b1621a93
```

Add a scope:

```text
Scope name: access_as_user
Who can consent: Admins and users
Admin consent display name: Access Sentinel
Admin consent description: Allows Sentinel to call its backend API as the signed-in user.
User consent display name: Access Sentinel
User consent description: Allows Sentinel to call its backend API as you.
State: Enabled
```

## API Permissions

In the same app registration, open **API permissions**.

Add permission:

```text
My APIs -> Sentinel Vaultrix -> access_as_user
```

Grant admin consent if your tenant requires it.

## App Roles

Open **App roles** and create:

```text
Display name: Admin
Value: Admin
Allowed member types: Users/Groups
Description: Full Sentinel administration access
Enabled: Yes
```

```text
Display name: Platform Engineer
Value: Platform Engineer
Allowed member types: Users/Groups
Description: Can onboard resources and manage governance workflows
Enabled: Yes
```

```text
Display name: Viewer
Value: Viewer
Allowed member types: Users/Groups
Description: Read-only Sentinel access
Enabled: Yes
```

Assign your user to `Admin` from:

```text
Enterprise applications -> Sentinel Vaultrix -> Users and groups
```

## Runtime Values

Backend:

```env
DEMO_MODE=false
APP_NAME=Sentinel
APP_BASE_URL=https://sentinel.vaultrix.in
API_BASE_URL=https://sentinel.vaultrix.in
AZURE_TENANT_ID=61d2b850-89ba-4674-9fc4-42d9ff6bdaa5
AZURE_CLIENT_ID=14467cba-ecd6-4f59-a06c-b5d1b1621a93
AZURE_API_AUDIENCE=api://14467cba-ecd6-4f59-a06c-b5d1b1621a93
AZURE_ALLOWED_TENANTS=61d2b850-89ba-4674-9fc4-42d9ff6bdaa5
AZURE_AUTHORITY=https://login.microsoftonline.com/61d2b850-89ba-4674-9fc4-42d9ff6bdaa5/v2.0
AZURE_OPERATION_AUTH_MODE=default_credential
BACKEND_CORS_ORIGINS=["https://sentinel.vaultrix.in","http://sentinel.vaultrix.in"]
```

Frontend:

```env
NEXT_PUBLIC_DEMO_MODE=false
NEXT_PUBLIC_API_BASE_URL=/api/v1
NEXT_PUBLIC_AZURE_TENANT_ID=61d2b850-89ba-4674-9fc4-42d9ff6bdaa5
NEXT_PUBLIC_AZURE_CLIENT_ID=14467cba-ecd6-4f59-a06c-b5d1b1621a93
NEXT_PUBLIC_AZURE_API_SCOPE=api://14467cba-ecd6-4f59-a06c-b5d1b1621a93/access_as_user
NEXT_PUBLIC_AZURE_REDIRECT_URI=https://sentinel.vaultrix.in/auth/callback
```
