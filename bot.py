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

# Function to bypass gplinks URL
def gplinks_bypass(url: str):
    client = cloudscraper.create_scraper(allow_brotli=False)
    domain = "https://gplinks.co/"
    referer = "https://mynewsmedia.co/"

    # Initial request to get the 'vid' parameter
    response = client.get(url, allow_redirects=False)
    vid = response.headers.get("Location", "").split("=")[-1]
    if not vid:
        return "Could not retrieve the vid from URL."

    # Construct the URL with the 'vid' parameter
    url = f"{url}/?{vid}"

    # Second request to get the page with the form
    response = client.get(url, allow_redirects=False)
    soup = BeautifulSoup(response.content, "html.parser")

    # Extract input data from the form
    form = soup.find(id="go-link")
    if not form:
        return "Form with ID 'go-link' not found."
    
    inputs = form.find_all(name="input")
    data = {input.get('name'): input.get('value') for input in inputs}

    # Wait for a few seconds before making the next request
    time.sleep(10)
    
    # Headers required for bypassing the protection
    headers = {"x-requested-with": "XMLHttpRequest"}
    response = client.post(domain + "links/go", data=data, headers=headers)

    # Check if the response contains the 'url' key
    if response.status_code == 200 and "url" in response.json():
        return response.json()["url"]
    else:
        return "Bypass failed, could not retrieve the final URL."

# Handler function for incoming messages
@app.on_message(filters.text & filters.private)
def handle_message(client, message):
    text = message.text.strip()  # Remove any leading/trailing whitespace
    if "gplinks.co" in text:
        message.reply_text("Processing your request, please wait...")  # Inform the user that the process has started
        try:
            final_url = gplinks_bypass(text)  # Call the bypass function
            message.reply_text(f"Final URL: {final_url}")
        except Exception as e:
            message.reply_text(f"An error occurred: {str(e)}")
    else:
        message.reply_text("Please send a valid gplinks.co URL.")

if __name__ == "__main__":
    app.run()
