from fastapi import FastAPI

from app.api.routers import ALL_ROUTERS
from app.lifespan import lifespan
from app.settings import settings

app = FastAPI(title=settings.app.name, lifespan=lifespan)

for router in ALL_ROUTERS:
    app.include_router(router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host=settings.app.host, port=settings.app.port, reload=True)
