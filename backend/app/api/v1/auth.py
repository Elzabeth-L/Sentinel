from fastapi import APIRouter, Depends

from app.api.deps import get_current_principal
from app.core.security import get_token_validator
from app.schemas.auth import AuthenticatedPrincipal

router = APIRouter()


@router.get("/me", response_model=AuthenticatedPrincipal)
def me(principal: AuthenticatedPrincipal = Depends(get_current_principal)) -> AuthenticatedPrincipal:
    return principal


@router.get("/openid-configuration")
async def openid_configuration() -> dict[str, object]:
    return await get_token_validator().openid_configuration()

