from datetime import datetime

from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.document import Document
from app.models.document import DocumentStatus
from app.schemas.documents import DocumentCreateRequest
from app.models.job import JobType


class DocumentRepository:

    async def create_document(self, async_session: AsyncSession, payload: DocumentCreateRequest) -> int:
        dt_now = datetime.now()
        document = insert(Document).values(dataset_id=payload.dataset_id,
                            status=DocumentStatus.UPLOADED,
                            title=payload.title,
                            source_type=JobType.DOCUMENT_INGESTION,
                            source_url=payload.source_url,
                            created_at=dt_now,
                            updated_at=dt_now).returning(Document.id)
        result = await async_session.execute(document)
        return result.fetchone()[0]

