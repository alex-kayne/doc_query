import asyncpg
from redis.asyncio import Redis
from fastapi import APIRouter, Response
from starlette import status

from app.settings import settings

router = APIRouter()

RESPONSE_ERROR = {"status": "error"}

@router.get("/health")
async def health():
    return {"status": "ok"}

async def _check_postgres() -> bool:
    try:
        conn = await asyncpg.connect(user=settings.database.user, password=settings.database.password,
                                     database=settings.database.name, host=settings.database.host, port=settings.database.port)
        await conn.fetchval("SELECT 1")
        return True
    except Exception as e:
        return False
    finally:
        if conn is not None:
            await conn.close()

async def _check_redis() -> bool:
    try:
        r = Redis(host=settings.redis.host, port=settings.redis.port)
        await r.ping()
        return True
    except Exception as e:
        return False
    finally:
        if r:
            await r.aclose()


@router.get("/ready")
async def ping(response: Response):
    if not await _check_postgres():
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return RESPONSE_ERROR
    if not await _check_redis():
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return RESPONSE_ERROR
    return {"status": "ready"}