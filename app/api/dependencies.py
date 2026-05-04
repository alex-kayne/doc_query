from app.clients.arq import ArqClient
from app.repositories.dataset import DatasetRepository
from app.repositories.document import DocumentRepository
from app.repositories.job import JobRepository
from app.services.dataset import DatasetService
from app.services.document_job import DocumentJobService


def get_document_job_service() -> DocumentJobService:
    return DocumentJobService(DocumentRepository(), JobRepository(), ArqClient())


def get_dataset_service() -> DatasetService:
    return DatasetService(DatasetRepository())
