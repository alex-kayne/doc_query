from pydantic import BaseModel, model_validator


class ChunkCreate(BaseModel):
    chunk_index: int
    chunk_text: str
    chunk_hash: str
    token_count: int
    embedding: list[float] | None = None
