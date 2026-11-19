from fastapi import FastAPI

from app.api.routes import documents

app = FastAPI(title="AI Document Assistant", version="0.1.0")
app.include_router(documents.router, prefix="/api/v1")


@app.get("/api/v1/health")
def health() -> dict[str, str]:
    return {"status": "ok"}