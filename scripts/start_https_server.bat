@echo off
REM Start Django HTTPS Server
echo ============================================================
echo    Starting Django HTTPS Development Server
echo ============================================================
echo.
echo Access your application at:
echo   https://localhost:8000/login/
echo   https://127.0.0.1:8000/login/
echo.
echo Note: Browser will show security warning for self-signed cert
echo       Click "Advanced" -> "Proceed anyway"
echo ============================================================
echo.

python manage.py runsslserver --certificate cert.pem --key key.pem 0.0.0.0:8000

pause
