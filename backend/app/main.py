from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.logging import configure_logging
from app.web_console import router as web_console_router


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    configure_logging()
    if settings.auto_create_schema:
        from app.db.session import create_schema

        create_schema()
    yield


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="Operational governance and resource optimization intelligence layer for AKS.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.backend_cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "X-Request-ID"],
)

app.include_router(web_console_router)
app.include_router(api_router, prefix="/api/v1")
app.mount("/metrics", make_asgi_app())
