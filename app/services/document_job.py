from app.clients.arq import ArqClient
from app.db.session import async_session_maker
from app.repositories.document import DocumentRepository
from app.repositories.job import JobRepository
from app.schemas.documents import DocumentCreateRequest


class DocumentJobService:
    def __init__(self, document_repository: DocumentRepository, job_repository: JobRepository, arq_client: ArqClient):
        self.document_repository = document_repository
        self.job_repository = job_repository
        self.arq_client = arq_client

    async def create_document(self, payload: DocumentCreateRequest) -> tuple[int, int]:
        async with async_session_maker() as session:
            async with session.begin():
                document_id = await self.document_repository.create_document(session, payload)
                job_id = await self.job_repository.create_job(session, document_id)
        await self.arq_client.enqueue_document_job(job_id)

        return document_id, job_id
