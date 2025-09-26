import discord
from discord.ext import commands
import json
import asyncio
import os
import sys
import pathlib # Used to resolve file paths reliably

# --- CONFIG LOADING FIX ---
# Determine the absolute path to the directory containing main.py
BASE_DIR = pathlib.Path(__file__).parent
CONFIG_PATH = BASE_DIR / "config.json"

# Load config
try:
    # Use the absolute path to config.json
    with open(CONFIG_PATH) as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: config.json not found at {CONFIG_PATH}. Please ensure it is in the same directory as main.py.")
    sys.exit(1)
# --------------------------

# We are no longer using config_channels.py, so remove the unused import
# from config_channels import stored_channel_ids 

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

# Load extensions from config
async def load_extensions():
    # Fix: Explicitly add the base directory to the system path for module loading
    if str(BASE_DIR) not in sys.path:
        sys.path.append(str(BASE_DIR))
        
    for module in config['default_modules']:
        try:
            # Load the module by its file name (without .py)
            await bot.load_extension(module)
            print(f"✅ Successfully loaded module: {module}")
        except Exception as e:
            # Handle the error specifically for debugging
            print(f"❌ Failed to load extension {module}: {e}")

# Entry point
async def main():
    async with bot:
        await load_extensions()
        await bot.start(config['token'])

asyncio.run(main())