from arq.connections import RedisSettings

from app.repositories.document import DocumentRepository
from app.repositories.ingestion_metrics import IngestionMetricsRepository
from app.repositories.job import JobRepository
from app.settings import settings
from app.services.job_worker import JobWorker
from app.workers.arq_tasks import process_document_job


async def startup(ctx) -> None:
    ctx["job_worker"] = JobWorker(
        job_repository=JobRepository(),
        document_repository=DocumentRepository(),
        ingestion_metrics_repository=IngestionMetricsRepository(),
    )
    return None


async def shutdown(ctx) -> None:
    return None


class ArqWorker:
    functions = [process_document_job, ]
    on_startup = startup
    on_shutdown = shutdown
    redis_settings = RedisSettings(host=settings.redis.host, port=settings.redis.port)
