import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import asyncio
from flask import Flask
from threading import Thread

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
APP_ID = os.getenv("APP_ID")
GUILD_ID = os.getenv("GUILD_ID")

app = Flask('')

@app.route('/')
def home():
    return "I'm alive!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()
# -------------------------------------------

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
        keep_alive()
        bot.run(TOKEN)