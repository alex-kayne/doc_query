import asyncio
from collections.abc import Iterable

from loguru import logger
from sqlalchemy import select

from app.db.session import async_session_maker
from app.models.job import Job

from app.services.jobs import JobsService
from app.services.ingestion_metrics import IngestionMetricsService

class JobWorker:
    def __init__(self, job_service: JobsService, ingestion_metrics_service: IngestionMetricsService):
        self.job_service = job_service
        self.ingestion_metrics_service = ingestion_metrics_service

    async def lookup_jobs(self) -> list[Job]:
        with async_session_maker() as session:
            jobs = select(Job).filter_by(status="pending")
            return session.scalar(jobs)

    async def process_jobs(self, jobs_list: Iterable[Job]):
        if not jobs_list:
            logger.info("Нет Jobs для выполнения")
            return None

        for job in jobs_list:
            try:
                await self.job_service.mark_job_processing()
                await self.ingestion_metrics_service.start_ingestion_metric()
                await asyncio.sleep(1)
                await self.job_service.mark_job_completed()
                await self.ingestion_metrics_service.finish_ingestion_metric_success()
            except:
                await self.job_service.mark_job_failed()
                await self.ingestion_metrics_service.finish_ingestion_metric_failed()


    async def run(self) -> None:
        with async_session_maker() as session:
            jobs = await self.lookup_jobs()
            return await self.process_jobs(jobs)
