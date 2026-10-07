from typing import Any
from ..utils.logger import get_logger

logger = get_logger(__name__)


class WebhookService:
    def process(self, event: dict[str, Any]) -> None:
        logger.info("Processing employee webhook event: %s", event.get("event", "unknown"))
