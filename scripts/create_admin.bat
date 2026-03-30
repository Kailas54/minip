@echo off
REM Create Django Superuser for Admin Panel Access
REM This allows you to view all database tables via web interface

echo ============================================================
echo    Creating Admin User for Database Viewer
echo ============================================================
echo.
echo This will create an admin account to access:
echo   - All users (CustomUser table)
echo   - All registered vehicles (RegisteredUser table)
echo   - All violations (UserViolation table)
echo.
echo You'll be able to view, search, filter, and edit data!
echo.
echo Running admin creation...
echo ============================================================
echo.

python manage.py createsuperuser

echo.
echo ============================================================
echo Admin user created successfully!
echo.
echo Next steps:
echo 1. Run: python manage.py runserver
echo 2. Open browser: http://localhost:8000/admin/
echo 3. Login with credentials you just created
echo 4. View all your database tables!
echo ============================================================
echo.
pause
