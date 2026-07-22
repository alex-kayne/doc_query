from app.api.routers.chunk import router as chunk_router
from app.api.routers.dataset import router as dataset_router
from app.api.routers.document import router as document_router
from app.api.routers.health import router as health_router

ALL_ROUTERS = (health_router, document_router, dataset_router,)
