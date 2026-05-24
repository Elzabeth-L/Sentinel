from functools import lru_cache

from pydantic import AnyHttpUrl, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AKS Governance Platform"
    app_env: str = "local"
    app_base_url: str = "http://localhost:3000"
    api_base_url: str = "http://localhost:8000"
    database_url: str = "postgresql+psycopg://aks_governance:aks_governance@localhost:5432/aks_governance"
    redis_url: str = "redis://localhost:6379/0"
    backend_cors_origins: list[str] = Field(default_factory=lambda: ["http://localhost:3000"])
    session_secret: str = "local-development-secret-change-me"
    demo_mode: bool = True
    auto_create_schema: bool = False
    log_level: str = "INFO"

    azure_tenant_id: str = "common"
    azure_client_id: str = ""
    azure_client_secret: str = ""
    azure_authority: AnyHttpUrl | str = "https://login.microsoftonline.com/common/v2.0"
    azure_api_audience: str = ""
    azure_allowed_tenants: list[str] = Field(default_factory=list)
    azure_operation_auth_mode: str = "default_credential"
    azure_subscription_ids: list[str] = Field(default_factory=list)

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @field_validator("backend_cors_origins", mode="before")
    @classmethod
    def parse_csv(cls, value: str | list[str]) -> list[str]:
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return value

    @field_validator("azure_allowed_tenants", mode="before")
    @classmethod
    def parse_tenant_csv(cls, value: str | list[str]) -> list[str]:
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return value

    @field_validator("azure_subscription_ids", mode="before")
    @classmethod
    def parse_subscription_csv(cls, value: str | list[str]) -> list[str]:
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return value


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
