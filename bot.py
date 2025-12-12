import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import asyncio

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
APP_ID = os.getenv("APP_ID")
GUILD_ID = os.getenv("GUILD_ID")

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.members = True  

class TranslatorBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="!",
            intents=intents,
            application_id=APP_ID
        )

    async def setup_hook(self):
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                await self.load_extension(f"cogs.{filename[:-3]}")

        await self.tree.sync()
        print("✔ Cogs and commands loaded.")

bot = TranslatorBot()

if __name__ == "__main__":
    if not TOKEN:
        print("DISCORD_TOKEN not found in .env")
    else:
        bot.run(TOKEN)
