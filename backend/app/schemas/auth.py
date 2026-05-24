from pydantic import BaseModel, computed_field

from app.core.rbac import ROLE_ORDER, Role


class AuthenticatedPrincipal(BaseModel):
    subject: str
    display_name: str
    email: str
    tenant_id: str
    roles: list[Role]
    scopes: list[str]
    expires_at: float

    @computed_field
    @property
    def highest_role(self) -> Role:
        return max(self.roles, key=lambda role: ROLE_ORDER[role])

