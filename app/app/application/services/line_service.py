from pydantic import BaseModel
from app.application.services.interfaces.i_line_service import ILineService


class LineWebhookRequest(BaseModel):
    destination: str
    events: list
    

class LineService(ILineService):
    async def handle_webhook(self, webhook_data: LineWebhookRequest):
        if not webhook_data.events:
            return {"message": "OK"}
        return {"message": "OK"}