# GPLinks Bypass

A script to bypass GPLinks URLs.

## Current Status

The script is currently unable to fully bypass GPLinks protection due to the following challenges:

1. The site requires CAPTCHA verification
2. Strong Cloudflare protection is in place
3. Anti-automation measures are implemented

## Possible Solutions

To successfully bypass GPLinks protection, one of these approaches would be needed:

1. Use a CAPTCHA solving service
2. Implement browser automation with manual CAPTCHA solving
3. Use a service like 2captcha or Anti-Captcha

## Technical Details

The current implementation:
1. Successfully connects to GPLinks
2. Handles CSRF tokens and cookies
3. Follows the correct request sequence
4. Gets blocked at the CAPTCHA verification step

## Requirements

```bash
pip install -r requirements.txt
```

## Note

This is a proof of concept that demonstrates the site's protection mechanisms. For actual use, you would need to implement CAPTCHA handling or use manual verification.
