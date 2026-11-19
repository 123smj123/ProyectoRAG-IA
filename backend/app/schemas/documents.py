from uuid import UUID

from pydantic import BaseModel


class PageText(BaseModel):
    page: int
    text: str


class DocumentUploadResponse(BaseModel):
    id: UUID
    filename: str
    page_count: int
    pages: list[PageText]