import asyncio

from app.db.session import async_session_maker
from app.models.document import DocumentStatus
from app.models.job import Job
from app.repositories.document import DocumentRepository
from app.repositories.job import JobRepository


class JobWorker:

    async def job_lookup(self, job_repository: JobRepository) -> tuple[int, int] | None:
        async with async_session_maker() as session:
            async with session.begin():
                job: Job | None = await job_repository.get_next_pending_job(session)
                if job:
                    return job.document_id, job.id
                else:
                    return None

    async def job_processing(self, job_id: int, document_id: int, job_repository: JobRepository,
                             document_repository: DocumentRepository) -> None:
        async with async_session_maker() as session:
            async with session.begin():
                await document_repository.update_status(session, document_id, DocumentStatus.PROCESSING)
                await job_repository.mark_processing_by(session, job_id)

                return None

    async def job_failed(self, job_id: int, document_id: int, error_message: str, job_repository: JobRepository,
                         document_repository: DocumentRepository) -> None:
        async with async_session_maker() as session:
            async with session.begin():
                await document_repository.update_status(session, document_id, DocumentStatus.FAILED)
                await job_repository.mark_failed_by(session, job_id, error_message)

                return None

    async def job_completed(self, job_id: int, document_id: int, job_repository: JobRepository,
                            document_repository: DocumentRepository) -> None:
        async with async_session_maker() as session:
            async with session.begin():
                await document_repository.update_status(session, document_id, DocumentStatus.READY)
                await job_repository.mark_completed_by(session, job_id)

                return None

    async def process_once(self, job_repository: JobRepository, document_repository: DocumentRepository) -> str:
        if not (job_ref := await self.job_lookup(job_repository)):
            return "Нет доступных задач для обработки документа"

        document_id: int = job_ref[0]
        job_id: int = job_ref[1]

        await self.job_processing(job_id, document_id, job_repository, document_repository)

        try:
            await asyncio.sleep(10)
        except Exception as e:
            error_message = e.__str__()
            await self.job_failed(job_id, document_id, error_message, job_repository, document_repository)
            return error_message

        await self.job_completed(job_id, document_id, job_repository, document_repository)
        return f"{job_id=} успешно обработано"
