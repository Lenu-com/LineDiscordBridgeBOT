import os
import aiohttp
from uvicorn import Config, Server
from fastapi import FastAPI, Request, Response
from linebot import WebhookParser
from linebot.models import TextMessage, MessageEvent
from aiolinebot import AioLineBotApi


app = FastAPI()
line_api = AioLineBotApi(channel_access_token=os.environ["LINE_CHANNEL_ACCESS_TOKEN"])
parser = WebhookParser(channel_secret=os.environ["LINE_CHANNEL_SECRET"])

# debug code
LINE_TARGET_GROUP_ID = None
DISCORD_TARGET_GUILD = None
DISCORD_TARGET_CHANNEL = None


async def format_message(event):
    username = await fetch_username(event)
    message_text = f'User: {username}\n\nMessage:\n{event.message.text}\n\nFrom: LINE'
    
    if hasattr(event.source, 'group_id') and event.source.group_id is not None:
        message_text += f'\nGroup: {await fetch_group_name(event.source.group_id)}'
        
    return message_text


async def fetch_group_name(group_id):
    access_token = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    url = f"https://api.line.me/v2/bot/group/{group_id}/summary"
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status != 200:
                print(f"Error: {response.status}")
                return None
            group_summary = await response.json()
            return group_summary.get("groupName")
                


async def fetch_username(event):
    user_id = event.source.user_id
    profile = await line_api.get_profile_async(user_id)
    return profile.display_name


async def send_message_to_discord(channel_id: int, message_text: str):
        from DiscordBotConnector import client
        await client.get_channel(channel_id).send(message_text)
        
        
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
        message_text = await format_message(event)
        await send_message_to_discord(DISCORD_TARGET_CHANNEL, message_text)
        
    return Response("ok", status_code=200)


async def line_bot_run():
    config = Config(app, host="0.0.0.0", port=8000, log_level="info")
    server = Server(config)
    await server.serve()