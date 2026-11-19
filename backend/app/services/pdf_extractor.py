import pymupdf

from app.schemas.documents import PageText


class PdfExtractionError(Exception):
    pass


def extract_pages(data: bytes) -> list[PageText]:
    """Extrae el texto por página desde los bytes del PDF (sin abrir ficheros en disco)."""
    try:
        with pymupdf.open(stream=data, filetype="pdf") as doc:
            if doc.needs_pass:
                raise PdfExtractionError("El PDF está protegido con contraseña.")
            return [
                PageText(page=number, text=page.get_text().strip())
                for number, page in enumerate(doc, start=1)
            ]
    except PdfExtractionError:
        raise
    except Exception as exc:
        raise PdfExtractionError("No se pudo leer el PDF.") from exc