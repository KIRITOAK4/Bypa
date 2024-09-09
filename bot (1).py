
import os
import requests
from pyrogram import Client, filters

API_ID = int(os.environ.get("API_ID", 14712540))
API_HASH = os.environ.get("API_HASH", "e61b996dc037d969a4f8cf6411bb6165")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "6202042878:AAFof9nGLi597vpEISpamG4b-d3Qsgp38Oc")

app = Client("url_bypass_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

def bypass_url(shortened_url):
    try:
        response = requests.get(shortened_url, allow_redirects=False)
        if response.status_code in [301, 302]:
            next_url = response.headers["Location"]
            return bypass_url(next_url)
        else:
            return shortened_url
    except Exception as e:
        return str(e)

@app.on_message(filters.command("bypass") & filters.private)
def bypass(client, message):
    if len(message.command) != 2:
        message.reply_text("Usage: /bypass <shortened_url>")
        return

    shortened_url = message.command[1]
    original_url = bypass_url(shortened_url)
    message.reply_text(f"Final URL: {original_url}")

if __name__ == "__main__":
    app.run()
