import uuid

from fastapi import APIRouter, HTTPException, UploadFile, status

from app.core.config import UPLOAD_PATH, settings
from app.schemas.documents import DocumentUploadResponse
from app.services.chunker import chunk_pages
from app.services.pdf_extractor import PdfExtractionError, extract_pages

router = APIRouter(prefix="/documents", tags=["documents"])

CHUNK_SIZE = 1024 * 1024


@router.post("", response_model=DocumentUploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(file: UploadFile) -> DocumentUploadResponse:
    max_bytes = settings.max_upload_size_mb * 1024 * 1024

    data = bytearray()
    while chunk := await file.read(CHUNK_SIZE):
        data.extend(chunk)
        if len(data) > max_bytes:
            raise HTTPException(
                status.HTTP_413_CONTENT_TOO_LARGE,
                f"El archivo supera el máximo de {settings.max_upload_size_mb} MB.",
            )

    # Validamos por contenido, no por extensión ni por Content-Type
    if not data.startswith(b"%PDF-"):
        raise HTTPException(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, "El archivo no es un PDF.")

    document_id = uuid.uuid4()
        # Primero validamos que el PDF se pueda leer; solo entonces lo guardamos en disco
    try:
        pages = extract_pages(bytes(data))
    except PdfExtractionError as exc:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, str(exc)) from exc

    document_id = uuid.uuid4()
    UPLOAD_PATH.mkdir(parents=True, exist_ok=True)
    path = UPLOAD_PATH / f"{document_id}.pdf"  # nombre aleatorio: nunca usamos el del cliente
    path.write_bytes(data)

    chunks = chunk_pages(pages, settings.chunk_size, settings.chunk_overlap)

    return DocumentUploadResponse(
        id=document_id,
        filename=file.filename or "document.pdf",
        page_count=len(pages),
        chunk_count=len(chunks),
        pages=pages,
        chunks=chunks,
    )