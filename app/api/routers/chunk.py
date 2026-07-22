from collections.abc import Sequence

from fastapi import APIRouter, Depends

from app.api.dependencies import get_dataset_service
from app.schemas.chunk import ChunkRetrieve, ChunkSearchResult
from app.services.chunk import ChunkService

router = APIRouter()


@router.post("/retrive", tags=["Чанки"])
async def retrieve_chunks(payload: ChunkRetrieve,
                          chunk_service: ChunkService = Depends(get_dataset_service)
                          ) -> Sequence[ChunkSearchResult]:
    return await chunk_service.fetch_chunks(payload)
