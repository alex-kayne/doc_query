from pydantic import BaseModel

class DocumentCreateRequest(BaseModel):
    dataset_id: int
    title: str
    source_type: str
    source_url: str | None

class DocumentCreateResponse(BaseModel):
    document_id: int
    job_id: int
    job_status: str
