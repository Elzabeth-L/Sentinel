from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.db.base import Base

engine = create_engine(settings.database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def create_schema() -> None:
    from app.models import audit, cluster, namespace, recommendation, user  # noqa: F401

    Base.metadata.create_all(bind=engine)

