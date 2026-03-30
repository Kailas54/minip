# Mobile Access Deployment Guide

## Overview
This guide explains how to host your Traffic Monitor application so you can access it from mobile phones.

## Quick Start - Local Network Access (Recommended for Testing)

### Option 1: Using ngrok (Easiest - Works Anywhere)

**Step 1: Install ngrok**
```bash
# Download from https://ngrok.com/download
# Or install via npm if you have Node.js
npm install -g ngrok
```

**Step 2: Run your Django server**
```bash
cd Helmet-Numberplate-Speed-Detection
python manage.py runserver
```

**Step 3: In a new terminal, start ngrok**
```bash
ngrok http 8000
```

**Step 4: Access from mobile**
- ngrok will display a URL like: `https://abc123.ngrok.io`
- Open this URL on any mobile browser
- **Pros**: Works from anywhere in the world, HTTPS enabled
- **Cons**: Free version has random URLs that change each session

---

### Option 2: Local Network Access (Same WiFi Only)

**Step 1: Find your computer's IP address**
```bash
# Windows
ipconfig

# Look for "IPv4 Address" - something like 192.168.1.100
```

**Step 2: Update settings.py**
```python
ALLOWED_HOSTS = ['*']  # Already configured
```

**Step 3: Run Django server with your IP**
```bash
python manage.py runserver 0.0.0.0:8000
```

**Step 4: Access from mobile**
- Make sure mobile is on the same WiFi network
- Open browser and go to: `http://YOUR_IP:8000`
- Example: `http://192.168.1.100:8000`
- **Pros**: No third-party service needed
- **Cons**: Only works on same network, no HTTPS

---

## Production Deployment (Recommended for Real Use)

### Option 3: Deploy to PythonAnywhere (Free Tier Available)

**Step 1: Create account**
- Go to https://www.pythonanywhere.com
- Sign up for free account

**Step 2: Upload your code**
```bash
# In your project directory
git init
git add .
git commit -m "Initial commit"

# Then follow PythonAnywhere's git instructions
```

**Step 3: Configure on PythonAnywhere**
1. Go to Web tab
2. Add a new web app
3. Choose Manual configuration
4. Python 3.10
5. Set paths:
   - Source code: `/home/yourusername/traffic-monitor`
   - Working directory: `/home/yourusername/traffic-monitor`
6. Configure WSGI configuration file
7. Set static files directories

**Step 4: Access from mobile**
- Your URL will be: `https://yourusername.pythonanywhere.com`
- Share this link with anyone

**Pros**: 
- Free hosting
- Always accessible
- HTTPS included
- No setup complexity

**Cons**: 
- Limited resources on free tier
- Need to renew manually every 3 months

---

### Option 4: Deploy to Render.com (Recommended)

**Step 1: Prepare your project**

Create a `render.yaml` file in your project root:

```yaml
services:
  - type: web
    name: traffic-monitor
    env: python
    buildCommand: "pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate"
    startCommand: "gunicorn mini.wsgi:application --bind 0.0.0.0:$PORT"
    envVars:
      - key: PYTHON_VERSION
        value: 3.10.0
      - key: DJANGO_SETTINGS_MODULE
        value: mini.settings
```

**Step 2: Update requirements.txt**
Add gunicorn:
```bash
echo "gunicorn==21.2.0" >> requirements.txt
```

**Step 3: Update settings.py for production**
```python
DEBUG = False
ALLOWED_HOSTS = ['*']  # Render will set the actual domain
```

**Step 4: Deploy**
1. Push code to GitHub
2. Go to https://render.com
3. Create account
4. Click "New +" → "Web Service"
5. Connect your GitHub repository
6. Render will auto-detect settings
7. Click "Create Web Service"

**Step 5: Access from mobile**
- You'll get a URL like: `https://traffic-monitor.onrender.com`
- Works from anywhere with HTTPS

**Pros**:
- Free tier available
- Automatic deployments
- HTTPS included
- More reliable than PythonAnywhere

**Cons**:
- Free tier sleeps after 15 min of inactivity

---

### Option 5: Deploy to Railway.app

**Step 1: Create account**
- Go to https://railway.app
- Sign up with GitHub

**Step 2: Deploy**
1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Choose your repository
4. Railway auto-detects Django
5. Add environment variable: `DJANGO_SETTINGS_MODULE=mini.settings`

**Step 3: Access**
- Get URL like: `https://yourproject.railway.app`

**Pros**:
- Very easy setup
- $5 free credit monthly
- Fast deployment

---

## Post-Deployment Configuration

### Update settings.py for Production

```python
# In mini/settings.py

DEBUG = False  # Important for security!

ALLOWED_HOSTS = [
    'yourdomain.com',
    'www.yourdomain.com',
    'yourproject.onrender.com',  # Replace with your actual domain
]

# Security settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

### Database Migration

After deploying, run migrations:
```bash
python manage.py migrate
```

### Collect Static Files

```bash
python manage.py collectstatic --noinput
```

---

## Mobile Optimization Features

Your app now includes:
✅ Mobile-responsive design
✅ Touch-friendly interface
✅ License number + Phone authentication (no email/password)
✅ Simple registration process
✅ Real-time violation tracking
✅ Bottom navigation for easy mobile use

---

## Testing Checklist

Before sharing with users:

1. ✅ Test registration on mobile
   - Enter license number and phone
   - Verify account creation works

2. ✅ Test login on mobile
   - Use license number + phone to login
   - Verify dashboard loads

3. ✅ Test video upload
   - Upload traffic video
   - Check violation detection works

4. ✅ Test vehicle registration
   - Register vehicle with phone number
   - Verify in database

5. ✅ Test on different devices
   - iOS Safari
   - Android Chrome
   - Different screen sizes

---

## Troubleshooting

### Can't access from mobile?

**Local Network:**
- Check firewall settings
- Ensure both devices on same WiFi
- Try disabling Windows Defender temporarily
- Use `ipconfig` to verify correct IP

**Production:**
- Check deployment logs
- Verify ALLOWED_HOSTS includes your domain
- Run `python manage.py check --deploy`

### Login not working?

- Clear browser cache
- Check database has users
- Verify session cookies enabled

### Static files not loading?

```bash
python manage.py collectstatic --noinput
```

Check STATIC_ROOT in settings.py

---

## Recommended Approach

**For Testing/Demo:**
Use **ngrok** - It's instant and works from anywhere

**For Production:**
Use **Render.com** or **Railway** - Professional hosting with HTTPS

**For Personal/Lab Use:**
Use **Local Network** - Simple but limited to same WiFi

---

## Quick Commands Reference

```bash
# Run local development server
python manage.py runserver 0.0.0.0:8000

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Check deployment readiness
python manage.py check --deploy

# Start ngrok tunnel
ngrok http 8000
```

---

## Support

If you encounter issues:
1. Check the console output for errors
2. Review Django logs
3. Verify database connections
4. Test on desktop first, then mobile

Good luck with your deployment! 🚀
