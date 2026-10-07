from datetime import date
from typing import Any


class Person:
    def __init__(self, first_name: str, last_name: str) -> None:
        self.first_name = first_name
        self.last_name = last_name


class Employee(Person):
    def __init__(self, **data: Any) -> None:
        super().__init__(data["first_name"], data["last_name"])
        self._data = dict(data)

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip()

    @property
    def age_of_record(self) -> int:
        joining = self._data.get("joining_date")
        if not joining:
            return 0
        try:
            year = date.fromisoformat(str(joining)).year
            return date.today().year - year
        except ValueError:
            return 0
