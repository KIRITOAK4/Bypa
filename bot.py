import os
import asyncio
import logging
from dotenv import load_dotenv
import cloudscraper
import time
from pyrogram import Client, filters
import aiohttp
from bs4 import BeautifulSoup
from datetime import datetime, timedelta


load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_ID = int(os.environ.get("API_ID", 14712540))
API_HASH = os.environ.get("API_HASH", "e61b996dc037d969a4f8cf6411bb6165")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "6280721521:AAGvEXRn-4tZD28vooWBiDZJuBxSErn4Xx0")

app = Client('gplinks_bypass_bot', api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

logger.info(f'Bot initialized with API_ID: {API_ID}')

@app.on_message(filters.command('start'))
async def start_command(client, message):
    await message.reply_text('Welcome! Send me a gplinks.co URL, and I\'ll bypass it for you. Use /help for more information.')

@app.on_message(filters.command('help'))
async def help_command(client, message):
    help_text = '''
    This bot bypasses gplinks.co URLs. Here's how to use it:
    
    1. Send a gplinks.co URL to the bot.
    2. The bot will process the URL and send you the bypassed link.
    
    Note: There's a limit of 5 requests per minute per user to prevent abuse.
    '''
    await message.reply_text(help_text)


async def gplinks(url: str):
    # Create a cloudscraper instance
    client = cloudscraper.create_scraper(allow_brotli=False)

    # Extract token from the URL
    token = url.split("/")[-1]
    domain = "https://gplinks.co/"
    referer = "https://safaroflink.com/"
    headers = {"Referer": referer}
    response = client.get(url, headers=headers, allow_redirects=False)
    
    if "Location" in response.headers:
        vid = response.headers["Location"].split("=")[-1]
    else:
        return "Failed to retrieve the video ID."
    url = f"{url}/?{pid}&{vid}"
    # Sleep for a while to mimic human behavior
    time.sleep(20)
    # Create a method to bypass cloudflare and after waiting for 5 sec get a Get link button 
    h = {"X-Requested-With": "XMLHttpRequest"}
    r = client.post(f"{domain}/links/go", data=data, headers=h)
    try:
        return r.json()["url"]
    except Exception as e:
        return f"Something went wrong: {e}"

# Example usage
url = "https://gplinks.co/073M"
bypassed_url = gplinks(url)
print(bypassed_url)
