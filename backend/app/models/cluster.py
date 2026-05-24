from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Cluster(Base):
    __tablename__ = "clusters"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    azure_resource_id: Mapped[str] = mapped_column(String(1000), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(255), index=True)
    subscription_id: Mapped[str] = mapped_column(String(64), index=True)
    resource_group: Mapped[str] = mapped_column(String(255), index=True)
    location: Mapped[str] = mapped_column(String(80))
    kubernetes_version: Mapped[str] = mapped_column(String(40))
    node_count: Mapped[int] = mapped_column(Integer, default=0)
    onboarding_state: Mapped[str] = mapped_column(String(40), default="Discovered")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

