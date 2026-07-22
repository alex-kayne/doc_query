from collections.abc import Sequence

from sqlalchemy import select, Row
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.document import DocumentChunk


class ChunkRepository:
    async def fetch_chunks_by_vector(self, async_session: AsyncSession, vector: list[float], top_k: int) -> Sequence[
        Row]:
        distance_expr = DocumentChunk.embedding.cosine_distance(vector).label("distance")
        stmt = select(DocumentChunk, distance_expr).where(DocumentChunk.embedding.isnot(None)).order_by(
            DocumentChunk.embedding.cosine_distance(vector)).limit(top_k)
        result = await async_session.execute(stmt)
        return result.all()
