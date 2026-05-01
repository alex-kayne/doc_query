from sqlalchemy import insert, update
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.ingestion_metric import IngestionMetric, IngestionMetricStatus


class IngestionMetricsRepository:
    async def start_metric(self, async_session: AsyncSession, job_id: int, document_id: int, stage: str) -> int:
        dt_now = datetime.now()
        metric = insert(IngestionMetric).values(document_id=document_id, job_id=job_id,
                                                status=IngestionMetricStatus.STARTED,
                                                stage=stage,
                                                started_at=dt_now, ).returning(IngestionMetric.id)
        result = await async_session.execute(metric)
        return result.fetchone()[0]

    async def finish_success(self, async_session: AsyncSession, metric_id: int, stage: str):
        dt_now = datetime.now()
        metric = update(IngestionMetric).where(IngestionMetric.id == metric_id).values(
            status=IngestionMetricStatus.SUCCESS,
            stage=stage,
            finished_at=dt_now, )
        await async_session.execute(metric)

    async def finish_failed(self, async_session: AsyncSession, metric_id: int, stage: str):
        dt_now = datetime.now()
        metric = update(IngestionMetric).where(IngestionMetric.id == metric_id).values(
            status=IngestionMetricStatus.FAILED,
            stage=stage,
            finished_at=dt_now, )
        await async_session.execute(metric)
