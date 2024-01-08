from fastapi import APIRouter, Depends, Request
from app.application.services.line_service import LineService, LineWebhookRequest
from app.application.services.factories.line_service_factory import LineServiceFactory


router = APIRouter()


@router.post("/ok")
async def ok(request: Request, line_service: LineService = Depends(LineServiceFactory.create)):
    webhook_data = await request.json()
    webhook_request = LineWebhookRequest(**webhook_data)
    return await line_service.handle_webhook(webhook_request)