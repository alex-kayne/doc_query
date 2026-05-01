from loguru import logger

from app.repositories.document import DocumentRepository
from app.repositories.job import JobRepository
from app.services.job_worker import JobWorker as ServiceJobWorker


class JobWorker:

    async def run(self) -> None:
        job_repository = JobRepository()
        document_repository = DocumentRepository()
        logger.info(await ServiceJobWorker().process_once(job_repository, document_repository))
        return None


if __name__ == '__main__':
    import asyncio

    asyncio.run(JobWorker().run())
