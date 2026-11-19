from pathlib import Path

import pymupdf
import pytest
from fastapi.testclient import TestClient

from app.api.routes import documents
from app.main import app

client = TestClient(app)


def make_pdf(texts: list[str]) -> bytes:
    doc = pymupdf.open()
    for text in texts:
        page = doc.new_page()
        page.insert_text((72, 72), text)
    data = doc.tobytes()
    doc.close()
    return data


def test_upload_pdf_extracts_text(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(documents, "UPLOAD_PATH", tmp_path)
    pdf = make_pdf(["Hola mundo", "Segunda pagina"])

    response = client.post(
        "/api/v1/documents", files={"file": ("test.pdf", pdf, "application/pdf")}
    )

    assert response.status_code == 201
    body = response.json()
    assert body["page_count"] == 2
    assert "Hola mundo" in body["pages"][0]["text"]
    assert len(list(tmp_path.glob("*.pdf"))) == 1


def test_rejects_non_pdf(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(documents, "UPLOAD_PATH", tmp_path)

    response = client.post(
        "/api/v1/documents",
        files={"file": ("fake.pdf", b"esto no es un pdf", "application/pdf")},
    )

    assert response.status_code == 415
    assert list(tmp_path.iterdir()) == []


def test_rejects_too_large(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(documents, "UPLOAD_PATH", tmp_path)
    monkeypatch.setattr(documents.settings, "max_upload_size_mb", 1)
    big = b"%PDF-" + b"0" * (1024 * 1024)

    response = client.post(
        "/api/v1/documents", files={"file": ("big.pdf", big, "application/pdf")}
    )

    assert response.status_code == 413