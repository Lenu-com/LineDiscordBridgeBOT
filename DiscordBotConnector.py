import os
import discord
from linebot.models import TextSendMessage

# debug code
LINE_TARGET_GROUP_ID = None
DISCORD_TARGET_GUILD = None
DISCORD_TARGET_CHANNEL = None


intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


async def send_message_to_line(to, message):
    from LINEBotConnector import line_api
    message_text = f'User: {message.author.name}\n\nMessage:\n{message.content}\n\nFrom: Discord\nServer: {message.guild.name}#{message.channel.name}'
    await line_api.push_message_async(to, TextSendMessage(text=message_text))
    
    
@client.event
async def on_message(message):
    if message.author.bot:
        return
    await send_message_to_line(LINE_TARGET_GROUP_ID, message)


async def discord_bot_run():
    await client.start(os.environ["DISCORD_API_KEY"])