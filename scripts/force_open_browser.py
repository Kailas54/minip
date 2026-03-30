"""
Force Open Login Page - Bypass Browser HTTPS Caching
This script finds your default browser and opens it with HTTP
"""

import webbrowser
import sys
import os

# URL to open
url = "http://127.0.0.1:8000/login/"

print("=" * 60)
print("Opening Login Page...")
print("=" * 60)
print()
print(f"URL: {url}")
print()

# Try to open with different browsers
browsers_to_try = [
    'chrome',
    'firefox', 
    'edge',
    'windows-default'
]

for browser_name in browsers_to_try:
    try:
        print(f"Trying {browser_name}...")
        browser = webbrowser.get(browser_name)
        browser.open(url)
        print(f"✓ Opened in {browser_name}!")
        print()
        print("If you see ERR_SSL_PROTOCOL_ERROR:")
        print("  1. Look at the address bar")
        print("  2. Change https:// to http://")
        print("  3. Press Enter")
        break
    except Exception as e:
        print(f"  {browser_name} not found, trying next...")
        continue
else:
    # Fallback to system default
    print("Opening with system default browser...")
    webbrowser.open(url)

print()
print("=" * 60)
print("IMPORTANT: Make sure address bar shows:")
print("  http://127.0.0.1:8000/login/")
print("NOT:")
print("  https://127.0.0.1:8000/login/")
print("=" * 60)
