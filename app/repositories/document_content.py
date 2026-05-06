from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.document import DocumentContent


class DocumentContentRepository:

    async def upsert_content(self, async_session: AsyncSession,
                             document_id: int,
                             normalized_text: str,
                             content_type: str,
                             content_hash: str) -> None:
        document_content = insert(DocumentContent).values(document_id=document_id,
                                                          normalized_text=normalized_text,
                                                          content_type=content_type,
                                                          content_hash=content_hash).on_conflict_do_update(
            constraint="document_content_document_id_key", set_=dict(normalized_text=normalized_text,
                                                                     content_type=content_type,
                                                                     content_hash=content_hash))

        await async_session.execute(document_content)
