from app.db.session import async_session_maker
from app.repositories.dataset import DatasetRepository
from app.schemas.datasets import DatasetCreateRequest


class DatasetService:
    def __init__(self, dataset_repository: DatasetRepository):
        self.dataset_repository = dataset_repository

    async def create_dataset(self, payload: DatasetCreateRequest) -> int:
        async with async_session_maker() as session:
            async with session.begin():
                data_set_id = await self.dataset_repository.create_dataset(session, payload)
        return data_set_id
