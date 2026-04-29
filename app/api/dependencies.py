from app.repositories.document import DocumentRepository
from app.repositories.job import JobRepository
from app.services.document_job import DocumentJobService


def get_document_repository() -> DocumentRepository:
    return DocumentRepository()


def get_job_repository() -> JobRepository:
    return JobRepository()


def get_document_job_service() -> DocumentJobService:
    return DocumentJobService(DocumentRepository(), JobRepository())
