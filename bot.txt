from pyrogram import Client, filters
from bs4 import BeautifulSoup
import time
import cloudscraper

# Your API credentials
API_ID = 14712540
API_HASH = "e61b996dc037d969a4f8cf6411bb6165"
BOT_TOKEN = "6202042878:AAFof9nGLi597vpEISpamG4b-d3Qsgp38Oc"

# Initialize Pyrogram Client
app = Client("gplinks_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

def gplinks(url: str):
    client = cloudscraper.create_scraper(allow_brotli=False)
    token = url.split("/")[-1]
    domain = "https://gplinks.co/"
    referer = "https://mynewsmedia.co/"
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

# Handler function for incoming messages
@app.on_message(filters.text & filters.private)
def handle_message(client, message):
    text = message.text.strip()  # Remove any leading/trailing whitespace
    if "gplinks.co" in text:
        message.reply_text("Processing your request, please wait...")  # Inform the user that the process has started
        try:
            final_url = gplinks(text)  # Call the bypass function
            message.reply_text(f"Final URL: {final_url}")
        except Exception as e:
            message.reply_text(f"An error occurred: {str(e)}")
    else:
        message.reply_text("Please send a valid gplinks.co URL.")

if __name__ == "__main__":
    app.run()
