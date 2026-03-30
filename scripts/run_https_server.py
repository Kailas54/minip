"""
Django Development Server with HTTPS Support
Run this instead of manage.py runserver for HTTPS access
"""

import os
import sys
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mini.settings')
django.setup()

# Import after Django setup
import uvicorn

if __name__ == '__main__':
    print("=" * 60)
    print("🔒 Starting Django Server with HTTPS")
    print("=" * 60)
    print()
    print("Access URLs:")
    print("  Secure: https://localhost:8000")
    print("  Also:   https://127.0.0.1:8000")
    print()
    print("Note: Browser may warn about self-signed certificate")
    print("      Click 'Proceed anyway' or 'Accept risk'")
    print("=" * 60)
    print()
    
    # Run with HTTPS using uvicorn
    uvicorn.run(
        "mini.asgi:application",
        host="0.0.0.0",
        port=8000,
        ssl_certfile="cert.pem",
        ssl_keyfile="key.pem",
        reload=False,  # Disable reload for stability
        log_level="info",
    )
