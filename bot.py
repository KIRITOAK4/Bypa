import os
import asyncio
import logging
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

async def bypass_gplinks(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            soup = BeautifulSoup(await response.text(), 'html.parser')
            
            # Find the button with id 'link-btn'
            link_btn = soup.find('a', id='link-btn')
            
            if link_btn:
                # Extract the 'href' attribute
                bypassed_url = link_btn.get('href')
                return bypassed_url
            else:
                return None

@app.on_message(filters.text & filters.regex(r'https?://gplinks\.co/\w+'))
async def handle_gplinks_url(client, message):
    url = message.text.strip()
    bypassed_url = await bypass_gplinks(url)
    
    if bypassed_url:
        await message.reply_text(f"Bypassed URL: {bypassed_url}")
    else:
        await message.reply_text("Sorry, I couldn't bypass this URL.")

async def main():
    await app.start()
    logger.info("Bot is running...")
    await asyncio.Event().wait()  # This will run forever

if __name__ == "__main__":
    asyncio.run(main())
