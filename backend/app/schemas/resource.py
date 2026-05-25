from pydantic import BaseModel, Field


class AzureResourceSummary(BaseModel):
    id: str
    name: str
    type: str
    resource_group: str = Field(alias="resourceGroup")
    subscription_id: str = Field(alias="subscriptionId")
    location: str
    kind: str | None = None
    tags: dict[str, str] = Field(default_factory=dict)

    model_config = {"populate_by_name": True}
