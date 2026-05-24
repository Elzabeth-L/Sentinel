from enum import StrEnum

from fastapi import HTTPException, status


class Role(StrEnum):
    admin = "Admin"
    platform_engineer = "Platform Engineer"
    viewer = "Viewer"


ROLE_ORDER = {
    Role.viewer: 1,
    Role.platform_engineer: 2,
    Role.admin: 3,
}


def require_role(user_role: Role, minimum_role: Role) -> None:
    if ROLE_ORDER[user_role] < ROLE_ORDER[minimum_role]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Requires {minimum_role} role or higher.",
        )

