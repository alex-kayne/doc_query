from app.db.session import async_session_maker
from app.models.document import DocumentStatus
from app.models.job import Job
from app.repositories.document import DocumentRepository
from app.repositories.document_chunk import DocumentChunkRepository
from app.repositories.document_content import DocumentContentRepository
from app.repositories.ingestion_metrics import IngestionMetricsRepository
from app.repositories.job import JobRepository
from app.schemas.chunk import ChunkCreate
from app.services.document_chunker import DocumentChunker
from app.services.document_parser import DocumentParser


class JobWorker:

    def __init__(self,
                 job_repository: JobRepository,
                 document_repository: DocumentRepository,
                 ingestion_metrics_repository: IngestionMetricsRepository,
                 document_content_repository: DocumentContentRepository,
                 document_chunker: DocumentChunker,
                 document_chunk_repository: DocumentChunkRepository) -> None:
        self.job_repository = job_repository
        self.document_repository = document_repository
        self.ingestion_metrics_repository = ingestion_metrics_repository
        self.document_content_repository = document_content_repository
        self.document_chunker = document_chunker
        self.document_chunk_repository = document_chunk_repository

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

    async def _upsert_document_content(self, document_id: int,
                                       normalized_text: str,
                                       content_type: str,
                                       content_hash: str,
                                       metric_id: int,
                                       job_id: int) -> None:
        async with async_session_maker() as session:
            async with session.begin():
                content_id = await self.document_content_repository.upsert_content(session, document_id,
                                                                                   normalized_text,
                                                                                   content_type,
                                                                                   content_hash)
                chunks = self.document_chunker.chunk(normalized_text)
                await self.document_chunk_repository.delete_by_content_id(session, content_id)
                await self.document_chunk_repository.bulk_insert_chunks(session, document_id, content_id, chunks)
                await self.document_repository.update_status(session, document_id, DocumentStatus.READY)
                await self.job_repository.mark_completed_by(session, job_id)
                await self.ingestion_metrics_repository.finish_success(session, metric_id, "ingestion")

    async def _delete_content_upsert_chunks_job_completed(self, content_id: int,
                                                          document_id: int,
                                                          chunks: list[ChunkCreate],
                                                          job_id: int,
                                                          metric_id: int) -> None:
        async with async_session_maker() as session:
            async with session.begin():
                await self.document_chunk_repository.delete_by_content_id(session, content_id)
                await self.document_chunk_repository.bulk_insert_chunks(session, document_id, content_id, chunks)
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
            normalized_text, text_hash = DocumentParser.parse("dummy", "docx")
            await self._upsert_document_content(document_id, normalized_text, "docx", text_hash, metric_id, job_id)
        except Exception as e:
            error_message = e.__str__()
            await self._job_failed(job_id, document_id, metric_id, error_message)
            return error_message

        return f"{job_id=} успешно обработано"
