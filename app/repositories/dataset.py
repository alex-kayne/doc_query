from datetime import datetime

from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.dataset import Dataset
from app.schemas.datasets import DatasetCreateRequest


class DatasetRepository:

    async def create_dataset(self, async_session: AsyncSession, payload: DatasetCreateRequest) -> int:
        dataset = insert(Dataset).values(name=payload.name,
                                         description=payload.description,
                                         created_at=datetime.now()).returning(Dataset.id)
        result = await async_session.execute(dataset)
        return result.fetchone()[0]
