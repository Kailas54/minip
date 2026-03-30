#!/usr/bin/env python
"""
Production Startup Script for Traffic Monitor
Run this to start the server with mobile access enabled
"""

import os
import socket
import sys
from pathlib import Path

def get_local_ip():
    """Get the local IP address of this machine"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def main():
    # Get project directory
    project_dir = Path(__file__).parent
    
    # Change to project directory
    os.chdir(project_dir)
    
    # Get local IP
    local_ip = get_local_ip()
    
    print("\n" + "="*60)
    print("🚦 TRAFFIC MONITOR - Starting Server")
    print("="*60)
    print(f"\n📱 Mobile Access Instructions:")
    print(f"   Local Access: http://localhost:8000")
    print(f"   Network Access: http://{local_ip}:8000")
    print(f"\n💡 To access from mobile:")
    print(f"   1. Connect mobile to same WiFi network")
    print(f"   2. Open browser and go to: http://{local_ip}:8000")
    print(f"\n🔒 Login Credentials:")
    print(f"   - Use License Number and Phone Number")
    print(f"   - No email/password required!")
    print("\n" + "="*60)
    print("\nStarting Django development server...\n")
    
    # Run Django server
    os.system('python manage.py runserver 0.0.0.0:8000')

if __name__ == '__main__':
    main()
