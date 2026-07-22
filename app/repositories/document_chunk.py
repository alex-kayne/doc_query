from datetime import datetime

from sqlalchemy import delete, insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.document import DocumentChunk
from app.schemas.chunk import ChunkCreate


class DocumentChunkRepository:

    async def delete_by_content_id(self, session: AsyncSession, content_id: int) -> None:
        delete_chunk = delete(DocumentChunk).where(DocumentChunk.content_id == content_id)
        await session.execute(delete_chunk)
        return None

    async def bulk_insert_chunks(self, session: AsyncSession, document_id: int, content_id: int,
                                 chunks: list[ChunkCreate]) -> None:
        dt_now = datetime.now()
        payload = [{
            "document_id": document_id,
            "content_id": content_id,
            "chunk_index": chunk.chunk_index,
            "chunk_text": chunk.chunk_text,
            "chunk_hash": chunk.chunk_hash,
            "token_count": chunk.token_count,
            "created_at": dt_now,
            "updated_at": dt_now,
            "embedding": chunk.embedding,
        } for chunk in chunks]
        await session.execute(insert(DocumentChunk), payload)
        return None
