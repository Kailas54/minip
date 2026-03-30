"""
Start ngrok Tunnel for Django Server
This creates a public HTTPS URL that forwards to your local server
"""

from pyngrok import ngrok, conf
import time
import webbrowser

# Stop any existing tunnels
ngrok.kill()

print("=" * 60)
print("🚀 Starting ngrok Tunnel")
print("=" * 60)
print()

# Create a tunnel pointing to your local Django server
public_url = ngrok.connect(8000)

print(f"✅ ngrok tunnel started!")
print()
print("=" * 60)
print("YOUR PUBLIC HTTPS URL:")
print("=" * 60)
print()
print(f"🔗 {public_url}")
print()
print("=" * 60)
print()
print("This URL is:")
print("  ✅ Accessible from ANY device (desktop, mobile, tablet)")
print("  ✅ Uses real HTTPS (no certificate warnings!)")
print("  ✅ Works from anywhere in the world")
print("  ✅ Bypasses all browser HTTPS caching issues")
print()
print("=" * 60)
print()
print("Opening in browser...")
webbrowser.open(public_url)
print()
print("Keep this terminal open while using ngrok!")
print("Press Ctrl+C to stop the tunnel")
print("=" * 60)
print()

# Keep the script running
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n\nStopping ngrok tunnel...")
    ngrok.kill()
    print("Tunnel stopped.")
