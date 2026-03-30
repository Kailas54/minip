@echo off
REM Open Login Page in Browser - Bypass HTTPS Auto-Redirect
echo Opening login page...

REM Try to open Chrome with flags to disable HTTPS auto-redirect
start chrome.exe --disable-features=AutomaticHttps http://127.0.0.1:8000/login/

timeout /t 2 /nobreak > nul

REM If Chrome didn't work, try default browser
start http://127.0.0.1:8000/login/
