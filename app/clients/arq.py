from app.settings import settings
from arq import create_pool
from arq.connections import RedisSettings

REDIS_SETTINGS = RedisSettings(host=settings.redis.host, port=settings.redis.port)


class ArqClient:
    redis_pool = None

    @classmethod
    async def start(cls) -> None:
        cls.redis_pool = await create_pool(REDIS_SETTINGS)
        return None

    @classmethod
    async def close(cls) -> None:
        if cls.redis_pool is not None:
            await cls.redis_pool.close()
        return None

    async def enqueue_document_job(self, job_id: int) -> None:
        await self.redis_pool.enqueue_job("process_document_job", job_id)
        return None