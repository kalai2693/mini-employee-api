from fastapi import FastAPI, HTTPException
from .api.routes import router
from .api.webhooks import router as webhook_router
from .storage import StorageService, StorageError
from .config import DATA_FILE
from .utils.logger import get_logger

logger = get_logger(__name__)
app = FastAPI(title="Mini Employee Directory API", version="1.0.0")
app.include_router(router)
app.include_router(webhook_router)


@app.on_event("startup")
def startup() -> None:
    try:
        StorageService().ensure_file()
    except StorageError as exc:
        logger.exception("Startup failed: %s", exc)


@app.get("/health")
def health():
    try:
        storage = StorageService()
        records = storage.read()
        return {"status": "healthy", "data_file": str(DATA_FILE), "employee_count": len(records)}
    except StorageError as exc:
        raise HTTPException(503, str(exc)) from exc
