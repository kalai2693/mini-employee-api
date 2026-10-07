# Mini Employee Directory API

A modular FastAPI project implementing the Week 1 Python + Software Engineering assessment.

## Features
- Employee CRUD with Pydantic validation
- JSON persistence isolated in `storage.py`
- CSV and Excel batch import
- PDF profile text extraction using PyMuPDF
- External REST sync with `HTTPAdapter` + `Retry(total=3)`
- HMAC-SHA256 webhook with `BackgroundTasks`
- Centralized logging and custom `@log_execution`
- pathlib-based file operations
- pytest tests, Ruff, Black and pre-commit configuration

## 1. Setup
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate
pip install -r requirements.txt
copy .env.example .env   # Windows
# cp .env.example .env   # Linux/macOS
```

## 2. Run
```bash
uvicorn employee_api.main:app --reload
```
Open Swagger at `http://127.0.0.1:8000/docs`.

## 3. Test
```bash
pytest
```

## 4. Git workflow
## 4. Git workflow

```bash
# Employee CRUD
git checkout -b feature/employee-crud
git add .
git commit -m "feat: add employee CRUD"

# File import
git checkout master
git checkout -b feature/file-import
git add .
git commit -m "feat: add Excel importer"

# Webhook
git checkout master
git checkout -b feature/webhook
git add .
git commit -m "feat: add HMAC employee webhook"

# Bug fix example
git checkout master
git checkout -b fix/pdf-parsing-bug
git add .
git commit -m "fix: handle PDF parsing issue"

Never commit `.env`, `.venv`, logs, or production JSON data.

## Endpoint checklist
- GET /employees
- GET /employees/{id}
- POST /employees
- PUT /employees/{id}
- PATCH /employees/{id}
- DELETE /employees/{id}
- POST /employees/import/csv
- POST /employees/import/excel
- POST /employees/import/pdf
- POST /employees/sync
- POST /webhooks/employee
- GET /health

## HMAC example
Signature = `HMAC-SHA256(WEBHOOK_SECRET, raw_request_body)`, represented as a lowercase hex digest in `X-Signature`.

## Assessment mapping
The implementation follows the supplied assessment structure: modular source folders, Pydantic schemas, JSON storage, file ingestion, external API retries, webhook verification, tests, linting and Git workflow.
