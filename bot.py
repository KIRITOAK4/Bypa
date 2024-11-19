import os
import asyncio
import logging
import time
import cloudscraper
from pyrogram import Client, filters
import aiohttp
from bs4 import BeautifulSoup

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_ID = int(os.environ.get("API_ID", 14712540))
API_HASH = os.environ.get("API_HASH", "e61b996dc037d969a4f8cf6411bb6165")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "6280721521:AAGvEXRn-4tZD28vooWBiDZJuBxSErn4Xx0")

app = Client("gplinks_bypass_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

logger.info(f"Bot initialized with API_ID: {API_ID}")

@app.on_message(filters.command("start"))
async def start_command(client, message):
    await message.reply_text("Welcome! Send me a gplinks.co URL, and I'll bypass it for you.")

def gplinks(url: str):
    client = cloudscraper.create_scraper(allow_brotli=False)
    token = url.split("/")[-1]
    domain = "https://gplinks.co/"
    referer = "https://safaroflife.com/"
    vid = client.get(url, allow_redirects=False).headers["Location"].split("=")[-1]
    url = f"{url}/?{vid}"
    response = client.get(url, allow_redirects=False)
    soup = BeautifulSoup(response.content, "html.parser")
    inputs = soup.find(id="go-link").find_all(name="input")
    data = {input.get("name"): input.get("value") for input in inputs}
    time.sleep(10)
    headers = {"x-requested-with": "XMLHttpRequest"}
    bypassed_url = client.post(domain + "links/go", data=data, headers=headers).json()[
        "url"
    ]
    try:
        return bypassed_url
    except:
        return "Something went wrong :("
