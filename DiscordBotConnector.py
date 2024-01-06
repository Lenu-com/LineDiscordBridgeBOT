import os
import discord


intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


async def discord_bot_run():
    @client.event
    async def on_message(message):
        if message.author.bot:
            return

    await client.start(os.environ["DISCORD_API_KEY"])
