from app.api.routers.document import router as document_router
from app.api.routers.health import router as health_router

ALL_ROUTERS = (health_router, document_router, )