from fastapi import APIRouter, Depends

from app.api.dependencies import get_document_job_service
from app.models.job import JobStatus
from app.schemas.documents import DocumentCreateRequest, DocumentCreateResponse
from app.services.document_job import DocumentJobService

router = APIRouter()


@router.post("/document", tags=["Документы"])
async def create_document(payload: DocumentCreateRequest,
                          document_job_service: DocumentJobService = Depends(get_document_job_service)) -> DocumentCreateResponse:
    document_id, job_id = await document_job_service.create_document(payload)
    return DocumentCreateResponse(document_id=document_id, job_id=job_id, job_status=JobStatus.PENDING)
