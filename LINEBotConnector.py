import os
from uvicorn import Config, Server
from fastapi import FastAPI, Request, Response
from linebot import WebhookParser
from linebot.models import TextMessage, MessageEvent
from aiolinebot import AioLineBotApi


app = FastAPI()
line_api = AioLineBotApi(channel_access_token=os.environ["LINE_CHANNEL_ACCESS_TOKEN"])
parser = WebhookParser(channel_secret=os.environ["LINE_CHANNEL_SECRET"])

#debug code
LINE_TARGET_GROUP_ID = 'Target Group ID'


async def line_bot_run():
    @app.post("/messaging_api/handle_request")
    async def handle_request(request: Request):
        events = parser.parse(
            (await request.body()).decode("utf-8"),
            request.headers.get("X-Line-Signature", ""))

        for event in events:
            if not isinstance(event, MessageEvent):
                continue
            if not isinstance(event.message, TextMessage):
                continue
            await line_api.push_message_async(to=LINE_TARGET_GROUP_ID, messages=TextMessage(text=event.message.text))
            
        return Response("ok", status_code=200)


    config = Config(app, host="0.0.0.0", port=8000, log_level="info")
    server = Server(config)
    await server.serve()