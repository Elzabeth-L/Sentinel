from collections.abc import Generator

from fastapi import Depends, HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.rbac import Role, require_role
from app.core.security import get_token_validator
from app.db.session import SessionLocal
from app.schemas.auth import AuthenticatedPrincipal

bearer = HTTPBearer(auto_error=False)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_principal(
    credentials: HTTPAuthorizationCredentials | None = Security(bearer),
) -> AuthenticatedPrincipal:
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing bearer token.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return get_token_validator().validate(credentials.credentials)


def require_admin(
    principal: AuthenticatedPrincipal = Depends(get_current_principal),
) -> AuthenticatedPrincipal:
    require_role(principal.highest_role, Role.admin)
    return principal


def require_platform_engineer(
    principal: AuthenticatedPrincipal = Depends(get_current_principal),
) -> AuthenticatedPrincipal:
    require_role(principal.highest_role, Role.platform_engineer)
    return principal

