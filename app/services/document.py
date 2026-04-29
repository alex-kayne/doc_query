from app.repositories.document import DocumentRepository
from app.schemas.documents import DocumentCreateRequest


class DocumentService:
    def __init__(self, document_repository: DocumentRepository):
        self.document_repository = document_repository

    async def create_document(self, payload: DocumentCreateRequest):
        await self.document_repository.create_document(payload)
