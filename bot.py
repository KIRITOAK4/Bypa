import requests
import time
import json
from bs4 import BeautifulSoup
from typing import Optional, Dict, Any

class GPLinksError(Exception):
    """Custom exception for GPLinks bypass errors"""
    pass

class GPLinksBot:
    """Bot for bypassing GPLinks URLs"""
    
    def __init__(self):
        self.session = requests.Session()
        self.base_headers = {
            'authority': 'gplinks.co',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'accept-language': 'en-US,en;q=0.9',
            'referer': 'https://sabkiyojana.com/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
        }
    
    def _get_csrf_token(self) -> Optional[str]:
        """Get CSRF token from cookies"""
        return self.session.cookies.get('csrfToken')
    
    def _make_request(self, method: str, url: str, **kwargs) -> requests.Response:
        """Make HTTP request with error handling"""
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            raise GPLinksError(f"Request failed: {str(e)}")
    
    def _visit_referrer(self):
        """Visit referrer site to set up session"""
        try:
            self._make_request('GET', 'https://sabkiyojana.com/', headers=self.base_headers)
        except GPLinksError as e:
            print(f"Warning: Failed to visit referrer site: {str(e)}")
    
    def bypass(self, url: str) -> Optional[str]:
        """
        Attempt to bypass GPLinks URL
        
        Args:
            url: The GPLinks URL to bypass
            
        Returns:
            str: The bypassed URL if successful, None otherwise
            
        Raises:
            GPLinksError: If an error occurs during bypass attempt
        """
        try:
            print("Starting bypass process...")
            
            # Visit referrer first
            self._visit_referrer()
            
            # Get the initial page
            print("Getting initial page...")
            response = self._make_request('GET', url, headers=self.base_headers)
            
            # Parse the page
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Get form data if available
            form = soup.find('form', {'id': 'go-link'})
            form_data = {}
            if form:
                print("Found go-link form")
                for input_tag in form.find_all('input'):
                    if input_tag.get('name'):
                        form_data[input_tag['name']] = input_tag.get('value', '')
            
            # Extract alias from URL
            alias = url.split('/')[-1]
            print(f"Using alias: {alias}")
            
            # Get CSRF token
            csrf_token = self._get_csrf_token()
            if csrf_token:
                print("Found CSRF token")
            
            # Wait for timer
            print("Waiting for timer...")
            time.sleep(15)
            
            # Prepare headers for bypass request
            bypass_headers = {
                **self.base_headers,
                'accept': 'application/json, text/javascript, */*; q=0.01',
                'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'origin': 'https://gplinks.co',
                'referer': url,
                'x-requested-with': 'XMLHttpRequest'
            }
            
            if csrf_token:
                bypass_headers['x-csrf-token'] = csrf_token
            
            # Make bypass request
            print("Making bypass request...")
            bypass_url = "https://gplinks.co/links/go"
            bypass_data = {
                'alias': alias,
                '_csrfToken': csrf_token if csrf_token else '',
                **form_data
            }
            
            bypass_response = self._make_request('POST', bypass_url, headers=bypass_headers, data=bypass_data)
            
            try:
                json_response = bypass_response.json()
                
                # Check for CAPTCHA requirement
                if json_response.get('status') == 'error' and 'captcha' in json_response.get('message', '').lower():
                    print("CAPTCHA verification required")
                    return None
                
                # Check for successful bypass
                if 'url' in json_response and json_response['url'].startswith('http'):
                    print("Successfully retrieved destination URL")
                    return json_response['url']
                
            except json.JSONDecodeError:
                print("Failed to parse bypass response")
            
            return None
            
        except GPLinksError as e:
            print(f"Error during bypass: {str(e)}")
            return None
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return None

def main():
    """Main function for testing"""
    bot = GPLinksBot()
    test_url = "https://gplinks.co/MuJ3H"
    result = bot.bypass(test_url)
    if result:
        print(f"Bypassed URL: {result}")
    else:
        print("Failed to bypass URL")

if __name__ == "__main__":
    main()
