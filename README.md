# RAG con IA

### Comandos para arrancar

#### Frontend:

```bash
cd frontend
npm install
npm run lint
npm run build
npm run dev
```

#### Backend:

```bash
python -m venv C:\venvs\ragia
C:\venvs\ragia\Scripts\Activate.ps1
pip install -r requirements-dev.txt
pytest
ruff check .
uvicorn app.main:app --reload
```
