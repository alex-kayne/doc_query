from datetime import datetime

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.document import Document
from app.models.document import DocumentStatus
from app.schemas.documents import DocumentCreateRequest


class DocumentRepository:

    async def create_document(self, async_session: AsyncSession, payload: DocumentCreateRequest) -> int:
        dt_now = datetime.now()
        document = insert(Document).values(dataset_id=payload.dataset_id,
                                           status=DocumentStatus.UPLOADED,
                                           title=payload.title,
                                           source_type=payload.source_type,
                                           source_url=payload.source_url,
                                           created_at=dt_now,
                                           updated_at=dt_now).returning(Document.id)
        result = await async_session.execute(document)
        return result.fetchone()[0]

    async def update_status(self, async_session: AsyncSession, document_id: int, status: DocumentStatus) -> None:
        document = select(Document).where(Document.id == document_id)
        result = await async_session.execute(document)
        document = result.scalar()
        document.status = status
