import asyncio
import logging
import os
import discord
from discord.ext import commands

logging.basicConfig(level=logging.INFO)

INTENTS = discord.Intents.default()
INTENTS.members = True
INTENTS.guilds = True
INTENTS.message_content = False

DEV_GUILD_ID = 1437847594675077224  

class AtlasBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=INTENTS)

    async def setup_hook(self):
        await self.load_extension("atlas_bot.features.events")

        try:
            await self.tree.sync(guild=discord.Object(id=DEV_GUILD_ID))
            print(f"[setup] Slash commands synced to guild {DEV_GUILD_ID}")
        except discord.Forbidden:
            await self.tree.sync()
            print("[setup] Guild sync forbidden; synced globally (may take a minute).")

bot = AtlasBot()

@bot.event
async def on_ready():
    print(f"[ready] Logged in as {bot.user} (ID: {bot.user.id})")

async def main():
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        raise SystemExit("Set DISCORD_TOKEN environment variable.")
    async with bot:
        await bot.start(token)

if __name__ == "__main__":
    asyncio.run(main())
