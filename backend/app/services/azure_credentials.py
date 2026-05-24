from functools import lru_cache

from azure.identity import DefaultAzureCredential
from azure.core.credentials import TokenCredential

from app.core.config import settings


@lru_cache
def get_azure_operation_credential() -> TokenCredential:
    if settings.azure_operation_auth_mode != "default_credential":
        raise ValueError(f"Unsupported Azure operation auth mode: {settings.azure_operation_auth_mode}")

    return DefaultAzureCredential(
        exclude_interactive_browser_credential=True,
        additionally_allowed_tenants=settings.azure_allowed_tenants or ["*"],
    )
