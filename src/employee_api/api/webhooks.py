import hashlib
import hmac
import json
from fastapi import APIRouter, BackgroundTasks, Header, HTTPException, Request
from ..config import WEBHOOK_SECRET
from ..services.webhook_service import WebhookService

router = APIRouter()
service = WebhookService()


@router.post("/webhooks/employee")
async def employee_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
    x_signature: str | None = Header(default=None),
):
    body = await request.body()
    if not x_signature:
        raise HTTPException(401, "Missing X-Signature")
    expected = hmac.new(WEBHOOK_SECRET.encode(), body, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected, x_signature):
        raise HTTPException(403, "Invalid signature")
    try:
        event = json.loads(body)
    except json.JSONDecodeError as exc:
        raise HTTPException(400, "Invalid JSON") from exc
    background_tasks.add_task(service.process, event)
    return {"status": "accepted"}
