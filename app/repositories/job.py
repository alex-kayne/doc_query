from datetime import datetime

from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.job import Job
from app.models.job import JobStatus
from app.models.job import JobType


class JobRepository:
    async def create_job(self, async_session: AsyncSession, document_id: int) -> int:
        dt_now = datetime.now()
        job = insert(Job).values(document_id=document_id,
                                 status=JobStatus.PENDING,
                                 type=JobType.DOCUMENT_INGESTION,
                                 attempts=0,
                                 created_at=dt_now,
                                 updated_at=dt_now).returning(Job.id)
        result = await async_session.execute(job)
        return result.fetchone()[0]
