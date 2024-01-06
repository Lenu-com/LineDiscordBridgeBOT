import asyncio
from DiscordBotConnector import discord_bot_run
from LINEBotConnector import line_bot_run


async def main():
    async with asyncio.TaskGroup() as tg:
        tg.create_task(discord_bot_run())
        tg.create_task(line_bot_run())
        
        
asyncio.run(main())