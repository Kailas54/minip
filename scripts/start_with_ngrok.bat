@echo off
REM Start Django Server with ngrok HTTPS Tunnel
echo ============================================================
echo    Starting Django + ngrok (HTTPS Access)
echo ============================================================
echo.
echo Step 1: Starting Django server on port 8000...
start "Django Server" cmd /k "cd Helmet-Numberplate-Speed-Detection && python manage.py runserver 0.0.0.0:8000"
timeout /t 3 /nobreak > nul

echo Step 2: Starting ngrok tunnel...
python start_ngrok.py

pause
