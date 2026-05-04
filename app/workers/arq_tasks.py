async def process_document_job(ctx, job_id: int) -> str:
    job_worker = ctx["job_worker"]
    return await job_worker.process_job(job_id)
