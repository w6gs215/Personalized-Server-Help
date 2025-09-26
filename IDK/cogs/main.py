import discord
from discord.ext import commands
import json
import asyncio
import os
import sys
import pathlib 

BASE_DIR = pathlib.Path(__file__).parent
CONFIG_PATH = BASE_DIR / "config.json"

try:
    with open(CONFIG_PATH) as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: config.json not found at {CONFIG_PATH}. Please ensure it is in the same directory as main.py.")
    sys.exit(1)
    
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=config['prefix'], intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user} (ID: {bot.user.id})")

    try:
        synced = await bot.tree.sync()
        print(f"🌐 Synced {len(synced)} global slash commands.")
    except Exception as e:
        print(f"❌ Failed to sync commands: {e}")

async def load_extensions():
    if str(BASE_DIR) not in sys.path:
        sys.path.append(str(BASE_DIR))
        
    for module in config['default_modules']:
        try:
            await bot.load_extension(module)
            print(f"✅ Successfully loaded module: {module}")
        except Exception as e:
            print(f"❌ Failed to load extension {module}: {e}")

async def main():
    async with bot:
        await load_extensions()
        await bot.start(config['token'])

asyncio.run(main())
