from app.schemas.documents import Chunk, PageText


def split_text(text: str, chunk_size: int, overlap: int) -> list[str]:
    """Divide un texto en fragmentos de ~chunk_size caracteres con solapamiento."""
    if chunk_size <= 0:
        raise ValueError("chunk_size debe ser mayor que 0")
    if not 0 <= overlap < chunk_size:
        raise ValueError("overlap debe estar entre 0 y chunk_size - 1")

    text = " ".join(text.split())  # normaliza espacios y saltos de línea
    if not text:
        return []
    if len(text) <= chunk_size:
        return [text]

    chunks: list[str] = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        if end < len(text):
            # retrocede hasta un espacio para no cortar palabras
            space = text.rfind(" ", start + chunk_size // 2, end)
            if space != -1:
                end = space

        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end >= len(text):
            break

        next_start = end - overlap
        if next_start <= start:  # garantiza que siempre avanzamos
            next_start = end
        while 0 < next_start < end and text[next_start - 1] != " ":
            next_start += 1  # no empezar a mitad de palabra
        start = next_start
    return chunks


def chunk_pages(pages: list[PageText], chunk_size: int, overlap: int) -> list[Chunk]:
    """Trocea cada página por separado, así cada fragmento conserva su página exacta."""
    chunks: list[Chunk] = []
    for page in pages:
        for text in split_text(page.text, chunk_size, overlap):
            chunks.append(Chunk(index=len(chunks), page=page.page, text=text))
    return chunks