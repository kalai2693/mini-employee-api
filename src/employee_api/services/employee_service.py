from typing import Any
from ..schemas.employee import EmployeeCreate, EmployeeUpdate
from ..storage import StorageService

class EmployeeNotFoundError(Exception): pass
class DuplicateEmailError(Exception): pass

class EmployeeService:
    def __init__(self, storage: StorageService) -> None:
        self.storage = storage

    def list(self, skip: int = 0, limit: int = 10) -> list[dict[str, Any]]:
        return self.storage.read()[skip:skip+limit]

    def get(self, employee_id: int) -> dict[str, Any]:
        for emp in self.storage.read():
            if emp["id"] == employee_id:
                return emp
        raise EmployeeNotFoundError

    def _unique(self, email: str, ignore_id: int | None = None) -> None:
        if any(e.get("email", "").lower() == email.lower() and e["id"] != ignore_id for e in self.storage.read()):
            raise DuplicateEmailError

    def create(self, payload: EmployeeCreate) -> dict[str, Any]:
        records = self.storage.read()
        self._unique(str(payload.email))
        new_id = max((e.get("id", 0) for e in records), default=0) + 1
        record = {"id": new_id, **payload.model_dump(mode="json")}
        records.append(record)
        self.storage.write(records)
        return record

    def replace(self, employee_id: int, payload: EmployeeCreate) -> dict[str, Any]:
        records = self.storage.read()
        self._unique(str(payload.email), employee_id)
        for i, e in enumerate(records):
            if e["id"] == employee_id:
                record = {"id": employee_id, **payload.model_dump(mode="json")}
                records[i] = record
                self.storage.write(records)
                return record
        raise EmployeeNotFoundError

    def update(self, employee_id: int, payload: EmployeeUpdate) -> dict[str, Any]:
        records = self.storage.read()
        for i, e in enumerate(records):
            if e["id"] == employee_id:
                changes = payload.model_dump(exclude_unset=True, mode="json")
                if "email" in changes: self._unique(changes["email"], employee_id)
                e.update(changes)
                records[i] = e
                self.storage.write(records)
                return e
        raise EmployeeNotFoundError

    def delete(self, employee_id: int) -> None:
        records = self.storage.read()
        filtered = [e for e in records if e["id"] != employee_id]
        if len(filtered) == len(records):
            raise EmployeeNotFoundError
        self.storage.write(filtered)
