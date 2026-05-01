from datetime import datetime

from sqlalchemy import insert, select, asc
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

    async def get_next_pending_job(self, async_session: AsyncSession) -> Job | None:
        job = select(Job).where(Job.status == JobStatus.PENDING).order_by(asc(Job.created_at)).limit(1)
        query_result = await async_session.execute(job)
        return query_result.scalar()

    async def mark_processing_by(self, async_session: AsyncSession, job_id: int):
        job_query = select(Job).where(Job.id == job_id)
        query_result = await async_session.execute(job_query)
        job = query_result.scalar_one_or_none()
        job.status = JobStatus.PROCESSING
        job.updated_at = datetime.now()

    async def mark_completed_by(self, async_session: AsyncSession, job_id: int):
        job_query = select(Job).where(Job.id == job_id)
        query_result = await async_session.execute(job_query)
        job = query_result.scalar_one_or_none()
        job.status = JobStatus.COMPLETED
        job.updated_at = datetime.now()

    async def mark_failed_by(self, async_session: AsyncSession, job_id: int, error_message: str):
        job_query = select(Job).where(Job.id == job_id)
        query_result = await async_session.execute(job_query)
        job = query_result.scalar_one_or_none()
        job.status = JobStatus.FAILED
        job.updated_at = datetime.now()
        job.error_message = error_message