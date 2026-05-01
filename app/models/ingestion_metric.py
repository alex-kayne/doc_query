from datetime import datetime, UTC
from enum import Enum

from sqlalchemy import Text, ForeignKey, Float, DateTime, Computed
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.db.base import Base


class IngestionMetricStatus(str, Enum):
    STARTED = "started"
    SUCCESS = "success"
    FAILED = "failed"


class IngestionMetric(Base):
    __tablename__ = "ingestion_metric"

    id: Mapped[int] = mapped_column(primary_key=True)
    document_id: Mapped[int] = mapped_column(ForeignKey("document.id"))
    job_id: Mapped[int] = mapped_column(ForeignKey("job.id"))
    status: Mapped[IngestionMetricStatus | None] = mapped_column(Text, nullable=True)
    stage: Mapped[str] = mapped_column(Text)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    duration_ms: Mapped[float | None] = mapped_column(Float,
                                                      Computed("EXTRACT(EPOCH FROM (finished_at - started_at)) * 1000"),
                                                      nullable=True, )
