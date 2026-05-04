from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.clients.arq import ArqClient


@asynccontextmanager
async def lifespan(app: FastAPI):
    await ArqClient.start()
    yield
    await ArqClient.close()