from collections.abc import Sequence
from app.schemas.chunk import ChunkSearchResult
from app.db.session import async_session_maker
from app.repositories.chunk import ChunkRepository
from app.schemas.chunk import ChunkRetrieve
from app.schemas.datasets import DatasetCreateRequest
from app.services.embedding_provider import FakeEmbeddingProvider


class ChunkService:
    def __init__(self, chunk_repository: ChunkRepository):
        self.chunk_repository = chunk_repository

    async def create_dataset(self, payload: DatasetCreateRequest) -> int:
        async with async_session_maker() as session:
            async with session.begin():
                data_set_id = await self.dataset_repository.create_dataset(session, payload)
        return data_set_id

    async def fetch_chunks(self, payload: ChunkRetrieve) -> Sequence[ChunkSearchResult]:
        request_embedding = (await FakeEmbeddingProvider.embed([payload.query]))[0]
        async with async_session_maker() as session:
            async with session.begin():
                return [ChunkSearchResult(chunk_id=row.DocumentChunk.id,
                                          chunk_text=row.DocumentChunk.chunk_text,
                                          document_id=row.DocumentChunk.document_id,
                                          distance=row.distance, ) for row in
                        await self.chunk_repository.fetch_chunks_by_vector(session, request_embedding, payload.top_k)]
