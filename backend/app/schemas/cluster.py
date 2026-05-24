from pydantic import BaseModel, Field


class ClusterSummary(BaseModel):
    id: str
    name: str
    subscription_id: str
    resource_group: str
    location: str
    kubernetes_version: str
    node_count: int
    onboarding_state: str = "Discovered"


class ClusterOnboardRequest(BaseModel):
    azure_resource_id: str = Field(min_length=10)
    display_name: str = Field(min_length=2, max_length=120)
    subscription_id: str = Field(min_length=12)
    resource_group: str = Field(min_length=1)
    location: str
    kubernetes_version: str
    node_count: int = Field(ge=1)

