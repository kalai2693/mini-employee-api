import json
from pathlib import Path
from typing import Any
from .config import DATA_FILE
from .utils.logger import get_logger

logger = get_logger(__name__)

class StorageError(Exception):
    """Raised when employee storage cannot be read or written."""

class StorageService:
    def __init__(self, data_file: Path = DATA_FILE) -> None:
        self.data_file = data_file

    def ensure_file(self) -> None:
        try:
            self.data_file.parent.mkdir(parents=True, exist_ok=True)
            if not self.data_file.exists():
                self.data_file.write_text("[]", encoding="utf-8")
            if not self.data_file.is_file():
                raise StorageError("Data path is not a file")
            with self.data_file.open("a", encoding="utf-8"):
                pass
        except (OSError, PermissionError) as exc:
            logger.exception("Storage startup failure")
            raise StorageError("Data file is missing or not writable") from exc

    def read(self) -> list[dict[str, Any]]:
        self.ensure_file()
        try:
            raw = self.data_file.read_text(encoding="utf-8")
            data = json.loads(raw)
            if not isinstance(data, list):
                raise ValueError("Employee data must be a JSON list")
            return data
        except (OSError, json.JSONDecodeError, ValueError) as exc:
            logger.exception("Storage read failure")
            raise StorageError("Employee data is corrupt or unreadable") from exc

    def write(self, records: list[dict[str, Any]]) -> None:
        self.ensure_file()
        try:
            tmp = self.data_file.with_suffix(".tmp")
            tmp.write_text(json.dumps(records, indent=2, default=str), encoding="utf-8")
            tmp.replace(self.data_file)
        except (OSError, TypeError) as exc:
            logger.exception("Storage write failure")
            raise StorageError("Employee data cannot be written") from exc
