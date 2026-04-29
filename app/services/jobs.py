
class JobsService:

    async def create_job(self, document_id: int, job_type: str):
        ...

    async def get_next_pending_job(self):
        ...

    async def mark_job_processing(self):
        ...

    async def mark_job_completed(self):
        ...

    async def mark_job_failed(self):
        ...