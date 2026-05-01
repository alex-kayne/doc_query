from loguru import logger

from app.repositories.document import DocumentRepository
from app.repositories.ingestion_metrics import IngestionMetricsRepository
from app.repositories.job import JobRepository
from app.services.job_worker import JobWorker as ServiceJobWorker


class JobWorker:

    async def run(self) -> None:
        job_repository = JobRepository()
        document_repository = DocumentRepository()
        ingestion_metrics_repository = IngestionMetricsRepository()
        logger.info(await ServiceJobWorker(job_repository, document_repository, ingestion_metrics_repository).process_once())
        return None


if __name__ == '__main__':
    import asyncio

    asyncio.run(JobWorker().run())
