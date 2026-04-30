from fastapi import APIRouter, Depends

from app.api.dependencies import get_dataset_service
from app.schemas.datasets import DatasetCreateRequest, DatasetCreateResponse
from app.services.dataset import DatasetService

router = APIRouter()


@router.post("/dataset", tags=["Датасеты"])
async def create_document(payload: DatasetCreateRequest,
                          dataset_service: DatasetService = Depends(get_dataset_service)) -> DatasetCreateResponse:
    dataset_id = await dataset_service.create_dataset(payload)
    return DatasetCreateResponse(dataset_id=dataset_id, name=payload.name)
