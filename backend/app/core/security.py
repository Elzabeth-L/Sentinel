from datetime import UTC, datetime
from functools import lru_cache
from typing import Any

import httpx
import jwt
from fastapi import HTTPException, status
from jwt import PyJWKClient

from app.core.config import settings
from app.core.rbac import Role
from app.schemas.auth import AuthenticatedPrincipal


class TokenValidator:
    def __init__(self) -> None:
        tenant = settings.azure_tenant_id or "common"
        self.issuer = f"https://login.microsoftonline.com/{tenant}/v2.0"
        self.jwks_url = f"https://login.microsoftonline.com/{tenant}/discovery/v2.0/keys"
        self.audience = settings.azure_api_audience or settings.azure_client_id
        self._jwk_client = PyJWKClient(self.jwks_url)

    def validate(self, token: str) -> AuthenticatedPrincipal:
        if settings.demo_mode and token == "demo-token":
            return AuthenticatedPrincipal(
                subject="demo-user",
                display_name="Demo Platform Engineer",
                email="demo@example.com",
                tenant_id="demo-tenant",
                roles=[Role.admin],
                scopes=["Cluster.Read", "Governance.Write"],
                expires_at=datetime.now(UTC).timestamp() + 3600,
            )

        try:
            signing_key = self._jwk_client.get_signing_key_from_jwt(token)
            claims: dict[str, Any] = jwt.decode(
                token,
                signing_key.key,
                algorithms=["RS256"],
                audience=self.audience,
                issuer=self.issuer,
                options={"require": ["exp", "iat", "iss", "aud"]},
            )
        except jwt.PyJWTError as exc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired bearer token.",
                headers={"WWW-Authenticate": "Bearer"},
            ) from exc

        tenant_id = claims.get("tid", "")
        if settings.azure_allowed_tenants and tenant_id not in settings.azure_allowed_tenants:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Tenant not allowed.")

        roles = [Role(role) for role in claims.get("roles", []) if role in Role]
        if not roles:
            roles = [Role.viewer]

        scopes = str(claims.get("scp", "")).split()
        return AuthenticatedPrincipal(
            subject=claims["sub"],
            display_name=claims.get("name", claims.get("preferred_username", "Unknown user")),
            email=claims.get("preferred_username", ""),
            tenant_id=tenant_id,
            roles=roles,
            scopes=scopes,
            expires_at=float(claims["exp"]),
        )

    async def openid_configuration(self) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(f"{settings.azure_authority}/.well-known/openid-configuration")
            response.raise_for_status()
            return response.json()


@lru_cache
def get_token_validator() -> TokenValidator:
    return TokenValidator()

