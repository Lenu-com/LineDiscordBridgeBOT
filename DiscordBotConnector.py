import os
import discord


async def discord_bot_run():
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_message(message):
        if message.author.bot:
            return
        await message.channel.send(message.content)

    await client.start(os.environ["DISCORD_API_KEY"])
