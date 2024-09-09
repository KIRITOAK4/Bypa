
from pyrogram import Client, filters
import requests
from bs4 import BeautifulSoup

API_ID = 14712540
API_HASH = "e61b996dc037d969a4f8cf6411bb6165"
BOT_TOKEN = "6202042878:AAFof9nGLi597vpEISpamG4b-d3Qsgp38Oc"

app = Client("gplinks_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

def bypass_gplinks(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    final_url = soup.find("a", {"id": "skip_button"})["href"]
    return final_url

@app.on_message(filters.text & filters.private)
def handle_message(client, message):
    text = message.text
    if "gplinks.com" in text:
        final_url = bypass_gplinks(text)
        message.reply_text(f"Final URL: {final_url}")
    else:
        message.reply_text("Please send a gplinks.com URL.")

if __name__ == "__main__":
    app.run()
