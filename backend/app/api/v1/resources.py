from fastapi import APIRouter, Depends

from app.api.deps import get_current_principal
from app.schemas.auth import AuthenticatedPrincipal
from app.schemas.resource import AzureResourceSummary
from app.services.azure_client import AzureInventoryClient

router = APIRouter()


@router.get("", response_model=list[AzureResourceSummary])
async def list_resources(
    principal: AuthenticatedPrincipal = Depends(get_current_principal),
) -> list[AzureResourceSummary]:
    return await AzureInventoryClient(principal).list_resources()
