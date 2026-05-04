import asyncio

from app.db.session import async_session_maker
from app.models.document import DocumentStatus
from app.models.job import Job
from app.repositories.document import DocumentRepository
from app.repositories.job import JobRepository
from app.repositories.ingestion_metrics import IngestionMetricsRepository


class JobWorker:

    def __init__(self, job_repository: JobRepository, document_repository: DocumentRepository,
                 ingestion_metrics_repository: IngestionMetricsRepository):
        self.job_repository = job_repository
        self.document_repository = document_repository
        self.ingestion_metrics_repository = ingestion_metrics_repository

    async def _job_lookup(self, job_id: int) -> tuple[int, int] | None:
        async with async_session_maker() as session:
            async with session.begin():
                job: Job | None = await self.job_repository.get_pending_job_by_id(session, job_id)
                if job:
                    return job.id, job.document_id
                else:
                    return None

    async def _job_processing(self, job_id: int, document_id: int) -> int:
        async with async_session_maker() as session:
            async with session.begin():
                await self.document_repository.update_status(session, document_id, DocumentStatus.PROCESSING)
                await self.job_repository.mark_processing_by(session, job_id)
                return await self.ingestion_metrics_repository.start_metric(session, job_id, document_id, "ingestion")


    async def _job_failed(self, job_id: int, document_id: int, metric_id: int, error_message: str) -> None:
        async with async_session_maker() as session:
            async with session.begin():
                await self.document_repository.update_status(session, document_id, DocumentStatus.FAILED)
                await self.job_repository.mark_failed_by(session, job_id, error_message)
                await self.ingestion_metrics_repository.finish_failed(session, metric_id, "ingestion")

                return None

    async def _job_completed(self, job_id: int, document_id: int, metric_id: int) -> None:
        async with async_session_maker() as session:
            async with session.begin():

                await self.document_repository.update_status(session, document_id, DocumentStatus.READY)
                await self.job_repository.mark_completed_by(session, job_id)
                await self.ingestion_metrics_repository.finish_success(session, metric_id, "ingestion")

                return None

    async def process_job(self, job_id: int) -> str:
        if not (job_ref := await self._job_lookup(job_id)):
            return f"{job_id=} отсутствует или находится не в статусе ожидание"

        job_id: int = job_ref[0]
        document_id: int = job_ref[1]

        metric_id = await self._job_processing(job_id, document_id)

        try:
            await asyncio.sleep(10)
        except Exception as e:
            error_message = e.__str__()
            await self._job_failed(job_id, document_id, metric_id, error_message)
            return error_message

        await self._job_completed(job_id, document_id, metric_id)
        return f"{job_id=} успешно обработано"
