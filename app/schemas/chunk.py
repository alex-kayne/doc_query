from pydantic import BaseModel, ConfigDict


class ChunkCreate(BaseModel):
    chunk_index: int
    chunk_text: str
    chunk_hash: str
    token_count: int
    embedding: list[float] | None = None


class ChunkRetrieve(BaseModel):
    query: str
    top_k: int = 5


class ChunkSearchResult(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    chunk_id: int
    chunk_text: str
    document_id: int
    distance: float
