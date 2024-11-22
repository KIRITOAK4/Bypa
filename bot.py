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
​
load_dotenv()
​
# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
​
API_ID = int(os.environ.get("API_ID", 14712540))
API_HASH = os.environ.get("API_HASH", "e61b996dc037d969a4f8cf6411bb6165")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "6280721521:AAGvEXRn-4tZD28vooWBiDZJuBxSErn4Xx0")
​
app = Client('gplinks_bypass_bot', api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
​
logger.info(f'Bot initialized with API_ID: {API_ID}')
​
# Store user request counts
user_requests = {}
​
def can_make_request(user_id):
    """Rate limiting: 5 requests per minute per user"""
    now = datetime.now()
    if user_id in user_requests:
        requests = [t for t in user_requests[user_id] if now - t < timedelta(minutes=1)]
        user_requests[user_id] = requests
        return len(requests) < 5
    return True
​
@app.on_message(filters.command('start'))
async def start_command(client, message):
    await message.reply_text('Welcome! Send me a gplinks.co URL, and I\'ll bypass it for you. Use /help for more information.')
​
@app.on_message(filters.command('help'))
async def help_command(client, message):
    help_text = '''
    This bot bypasses gplinks.co URLs. Here's how to use it:
    
    1. Send a gplinks.co URL to the bot.
    2. The bot will process the URL and send you the bypassed link.
    
    Note: There's a limit of 5 requests per minute per user to prevent abuse.
    '''
    await message.reply_text(help_text)
​
async def bypass_gplinks(url: str):
    """Bypass gplinks.co URLs"""
    try:
        # Create a cloudscraper instance
        client = cloudscraper.create_scraper(allow_brotli=False)
​
        # Get the initial page
        domain = "https://gplinks.co/"
        referer = "https://safaroflink.com/"
        headers = {"referer": referer}
        
        response = await asyncio.get_event_loop().run_in_executor(
            None, lambda: client.get(url, headers=headers, allow_redirects=False)
        )
​
        if response.status_code != 200:
            return None
​
        # Parse the page content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the countdown div and extract the target URL
        countdown = soup.find('div', {'class': 'countdown'})
        if not countdown:
            return None
​
        # Wait for the countdown (simulated)
        await asyncio.sleep(5)
​
        # Make the final request to get the destination URL
        dest_url = None
        try:
            data = {
                'method': 'bypass',
                'url': url
            }
            headers = {
                "X-Requested-With": "XMLHttpRequest",
                "referer": url
            }
            
            bypass_response = await asyncio.get_event_loop().run_in_executor(
                None, 
                lambda: client.post(f"{domain}links/bypass", data=data, headers=headers)
            )
            
            if bypass_response.status_code == 200:
                dest_url = bypass_response.json().get('url')
        except Exception as e:
            logger.error(f"Error in final bypass request: {e}")
            return None
​
        return dest_url
​
    except Exception as e:
        logger.error(f"Error bypassing URL: {e}")
        return None
​
@app.on_message(filters.regex(r'https?://gplinks\.co/\S+'))
async def handle_url(client, message):
    user_id = message.from_user.id
    
    # Check rate limit
    if not can_make_request(user_id):
        await message.reply_text("You've reached the request limit. Please wait a minute before trying again.")
        return
​
    # Update request count
    if user_id not in user_requests:
        user_requests[user_id] = []
    user_requests[user_id].append(datetime.now())
​
    # Send initial processing message
    status_message = await message.reply_text("Processing your URL... Please wait.")
​
    # Extract URL from message
    url = message.text.strip()
    
    # Try to bypass the URL
    bypassed_url = await bypass_gplinks(url)
    
    if bypassed_url:
        await status_message.edit_text(f"Here's your bypassed URL:\n{bypassed_url}")
    else:
        await status_message.edit_text("Sorry, I couldn't bypass this URL. Please make sure it's a valid gplinks.co URL.")
​
def main():
    logger.info("Starting bot...")
    app.run()
​
if __name__ == "__main__":
    main()
