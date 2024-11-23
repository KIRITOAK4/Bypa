import cloudscraper
import time
import json
from bs4 import BeautifulSoup

def bypass_gplinks(url: str):
    """Bypass gplinks.co URLs"""
    try:
        print("Starting bypass process...")
        
        # Create a cloudscraper session
        scraper = cloudscraper.create_scraper(
            browser={
                'browser': 'chrome',
                'platform': 'windows',
                'desktop': True
            }
        )
        
        # First visit the referrer site
        print("Visiting referrer site...")
        scraper.get('https://sabkiyojana.com/')
        
        # Get the initial page
        print("Getting initial page...")
        response = scraper.get(url)
        print(f"Initial response status: {response.status_code}")
        print(f"Initial cookies: {scraper.cookies.get_dict()}")
        
        # Parse the page
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Look for the form
        form = soup.find('form', {'id': 'go-link'})
        form_data = {}
        if form:
            print("\nFound go-link form")
            for input_tag in form.find_all('input'):
                if input_tag.get('name'):
                    form_data[input_tag['name']] = input_tag.get('value', '')
            print(f"Form data: {form_data}")
        
        # Extract alias from URL
        alias = url.split('/')[-1]
        print(f"\nUsing alias: {alias}")
        
        # Get CSRF token from cookies
        csrf_token = scraper.cookies.get('csrfToken')
        print(f"CSRF Token: {csrf_token}")
        
        # Wait for the initial timer
        print("\nWaiting for timer...")
        time.sleep(15)
        
        # Make the bypass request
        print("\nMaking bypass request...")
        bypass_url = "https://gplinks.co/links/go"
        headers = {
            'authority': 'gplinks.co',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://gplinks.co',
            'referer': url,
            'x-requested-with': 'XMLHttpRequest'
        }
        
        if csrf_token:
            headers['x-csrf-token'] = csrf_token
        
        bypass_data = {
            'alias': alias,
            '_csrfToken': csrf_token if csrf_token else '',
            **form_data
        }
        
        bypass_response = scraper.post(bypass_url, headers=headers, data=bypass_data)
        print(f"Bypass response status: {bypass_response.status_code}")
        print(f"Bypass response: {bypass_response.text}")
        
        try:
            json_response = bypass_response.json()
            if 'url' in json_response and json_response['url'].startswith('http'):
                print("\nSuccessfully retrieved destination URL")
                return json_response['url']
        except Exception as e:
            print(f"\nFailed to parse bypass response: {str(e)}")
        
        # Try to find any redirect URLs in the page
        try:
            for script in soup.find_all('script'):
                if script.string and 'window.location' in script.string:
                    redirect_url = script.string.split('window.location')[1].split('"')[1]
                    if redirect_url.startswith('http'):
                        print(f"\nFound redirect URL: {redirect_url}")
                        return redirect_url
        except:
            pass
        
        return None
        
    except Exception as e:
        print(f"Error in bypass_gplinks: {str(e)}")
        return None

if __name__ == "__main__":
    test_url = "https://gplinks.co/MuJ3H"
    print(f"Testing URL: {test_url}")
    result = bypass_gplinks(test_url)
    print(f"Final Result: {result}")
