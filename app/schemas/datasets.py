from pydantic import BaseModel


class DatasetCreateRequest(BaseModel):
    name: str
    description: str | None = None


class DatasetCreateResponse(BaseModel):
    dataset_id: int
    name: str
