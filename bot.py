
import os
import asyncio
import logging
from dotenv import load_dotenv
import cloudscraper
from pyrogram import Client, filters
import aiohttp
from bs4 import BeautifulSoup
from collections import defaultdict
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_ID = int(os.environ.get("API_ID", 14712540))
API_HASH = os.environ.get("API_HASH", "e61b996dc037d969a4f8cf6411bb6165")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "6280721521:AAGvEXRn-4tZD28vooWBiDZJuBxSErn4Xx0")

app = Client('gplinks_bypass_bot', api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

logger.info(f'Bot initialized with API_ID: {API_ID}')

# Rate limiting
rate_limit = defaultdict(lambda: {'count': 0, 'last_reset': datetime.now()})

def check_rate_limit(user_id, limit=5, window=60):
    now = datetime.now()
    user_data = rate_limit[user_id]
    
    if now - user_data['last_reset'] > timedelta(seconds=window):
        user_data['count'] = 0
        user_data['last_reset'] = now

    user_data['count'] += 1
    return user_data['count'] <= limit

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

async def fetch_url(url, headers=None):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, allow_redirects=False) as response:
            return await response.text(), response.headers

async def gplinks(url: str):
    """
    Bypass gplinks.co URL.
    :param url: str - The URL to be bypassed
    :return: str - The bypassed URL or an error message
    """
    try:
        client = cloudscraper.create_scraper(allow_brotli=False)
        domain = 'https://gplinks.co/'
        referer = 'https://safaroflife.com/'  # Example referer (adjust as needed)

        # Initial fetch to get token or vid
        resp, headers = await fetch_url(url)
        vid = headers.get('Location', '').split('=')[-1] if 'Location' in headers else None
        url = f"{url}/?{vid}" if vid else url

        # Second fetch to parse the form data
        resp, _ = await fetch_url(url)
        soup = BeautifulSoup(resp, 'html.parser')
        inputs = soup.find(id='go-link').find_all(name='input')
        data = {input_tag.get('name'): input_tag.get('value') for input_tag in inputs}

        # Respect cooldown
        await asyncio.sleep(10)

        # Send POST request to bypass URL
        headers = {'x-requested-with': 'XMLHttpRequest'}
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{domain}links/go", data=data, headers=headers) as response:
                bypassed_url = (await response.json()).get('url')

        return bypassed_url if bypassed_url else "Failed to bypass URL."
    except Exception as e:
        logger.error(f"Error in gplinks function: {str(e)}")
        return "An error occurred while bypassing the link."

@app.on_message(filters.text & filters.regex(r'https?://gplinks\.co/\S+'))
async def handle_gplinks_url(client, message):
    """
    Handle gplinks.co URLs sent by the user.
    """
    if not check_rate_limit(message.from_user.id):
        await message.reply_text('Rate limit exceeded. Please try again later.')
        return

    url = message.text.strip()
    await message.reply_text('Processing your request. Please wait...')

    try:
        bypassed_url = await gplinks(url)
        await message.reply_text(f"Here's your bypassed URL: {bypassed_url}")
    except Exception as e:
        logger.error(f"Error processing URL: {str(e)}")
        await message.reply_text('An error occurred while processing your request. Please try again later.')

if __name__ == '__main__':
    app.run()
