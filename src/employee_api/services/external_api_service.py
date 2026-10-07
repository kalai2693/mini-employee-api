from typing import Any
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from ..config import EXTERNAL_API_URL
from ..utils.logger import get_logger

logger=get_logger(__name__)

class ExternalAPIClient:
    def __init__(self, url: str = EXTERNAL_API_URL) -> None:
        self.url=url
        self.session=requests.Session()
        retry=Retry(total=3, backoff_factor=1, status_forcelist=[429,500,502,503,504],
                    allowed_methods=["GET"], raise_on_status=False)
        self.session.mount("http://", HTTPAdapter(max_retries=retry))
        self.session.mount("https://", HTTPAdapter(max_retries=retry))

    def fetch_employees(self) -> list[dict[str, Any]]:
        response=self.session.get(self.url, timeout=10)
        response.raise_for_status()
        payload=response.json()
        if isinstance(payload, list): return payload
        if isinstance(payload, dict):
            return payload.get("employees", [])
        raise ValueError("Unexpected external API payload")

    @staticmethod
    def extract_nested(data: dict[str, Any]) -> dict[str, Any]:
        employee=data.get("employee", {}) or {}
        profile=employee.get("profile", {}) or {}
        name=profile.get("name", {}) or {}
        contact=profile.get("contact", {}) or {}
        return {"first": name.get("first"), "last": name.get("last"), "email": contact.get("email")}
