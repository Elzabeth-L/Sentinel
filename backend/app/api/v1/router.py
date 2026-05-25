from fastapi import APIRouter

from app.api.v1 import auth, clusters, governance, health, recommendations, resources

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(clusters.router, prefix="/clusters", tags=["clusters"])
api_router.include_router(resources.router, prefix="/resources", tags=["resources"])
api_router.include_router(governance.router, prefix="/governance", tags=["governance"])
api_router.include_router(recommendations.router, prefix="/recommendations", tags=["recommendations"])
