@echo off
REM WebSocket-Enabled Server Startup Script
REM This starts the Django server with WebSocket support for vibration notifications

echo ============================================================
echo    TRAFFIC MONITOR - WebSocket Vibration System
echo ============================================================
echo.
echo Starting Django ASGI server with WebSocket support...
echo.
echo After server starts:
echo   1. Open mobile browser
echo   2. Go to: http://YOUR_IP:8000
echo   3. Login with License + Phone
echo   4. Dashboard will auto-connect to WebSocket
echo   5. Tap anywhere on page to enable vibrations
echo.
echo When violations are detected:
echo   - Mobile will vibrate in specific patterns
echo   - Visual notification will appear
echo   - Real-time alert via WebSocket!
echo.
echo Press Ctrl+C to stop the server
echo ============================================================
echo.

python manage.py runserver 0.0.0.0:8000

pause
