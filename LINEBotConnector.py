import os
import uvicorn
import fastapi
from linebot import WebhookParser
from linebot.models import TextMessage, MessageEvent
from aiolinebot import AioLineBotApi


async def line_bot_run():
    line_api = AioLineBotApi(channel_access_token=os.environ["LINE_CHANEL_ACCESS_TOKEN"])
    parser = WebhookParser(channel_secret=os.environ["LINE_CHANEL_SECRET"])
    app = fastapi.FastAPI()

    @app.post("/messaging_api/handle_request")
    async def handle_request(request: fastapi.Request):
        events = parser.parse(
            (await request.body()).decode("utf-8"),
            request.headers.get("X-Line-Signature", ""))

        for event in events:
            if not isinstance(event, MessageEvent):
                continue
            if not isinstance(event.message, TextMessage):
                continue

            await line_api.reply_message(event.reply_token, TextMessage(text=event.message.text))
        return "ok"

    config = uvicorn.Config(app, host="0.0.0.0", port=8000, log_level="info")
    server = uvicorn.Server(config)

    await server.serve()