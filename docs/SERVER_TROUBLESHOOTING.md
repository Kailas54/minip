# 🔧 Server Connection Troubleshooting Guide

## ❌ Problem: HTTPS Error

You saw this error:
```
code 400, message Bad request version
You're accessing the development server over HTTPS, but it only supports HTTP.
```

---

## ✅ Solution: Use HTTP Only

### Django Development Server Supports:
- ✅ **HTTP** (unencrypted)
- ❌ **NOT HTTPS** (no encryption support)

---

## 🌐 Correct URLs to Use

### From Desktop Browser:
```
http://localhost:8000
```

### From Mobile (Same WiFi):
```
http://YOUR_COMPUTER_IP:8000
```

Example:
```
http://192.168.1.100:8000
```

### From ngrok (Anywhere):
```
https://abc123.ngrok.io  # ngrok provides HTTPS
```

---

## 🔍 Why the Error Happened

### Possible Causes:

1. **Browser Auto-Redirect to HTTPS**
   - Some browsers automatically try HTTPS first
   - Solution: Manually type `http://` not `https://`

2. **HTTPS Everywhere Extension**
   - Browser extension forces HTTPS
   - Solution: Disable for localhost or use incognito mode

3. **Bookmarked HTTPS URL**
   - Old bookmark uses HTTPS
   - Solution: Delete bookmark and create new one with HTTP

4. **HSTS Preload**
   - Browser remembers site should use HTTPS
   - Solution: Clear browser data for that domain

---

## 🚀 Current Server Status

Your server is now running correctly:

```
✅ Running at: http://0.0.0.0:8000/
✅ Accessible from: All network interfaces
✅ Protocol: HTTP only
```

---

## 📱 How to Access

### Step 1: Find Your Computer's IP

**Windows:**
```bash
ipconfig
```

Look for **IPv4 Address** under your WiFi adapter:
```
Wireless LAN adapter Wi-Fi:
   IPv4 Address. . . . . . . . . . . : 192.168.1.100
```

### Step 2: Access from Mobile

1. **Connect mobile to same WiFi as computer**

2. **Open mobile browser** (Chrome recommended)

3. **Type EXACTLY:**
   ```
   http://192.168.1.100:8000
   ```
   
   ⚠️ **IMPORTANT:** 
   - Use `http://` NOT `https://`
   - Include `:8000` port number

4. **You should see login page!**

---

## 🔒 Security Note

### Development vs Production

**Development (Current):**
- HTTP only ✅
- No encryption
- For testing on trusted networks
- Don't expose to public internet directly

**Production (When Deployed):**
- HTTPS enabled ✅
- Encrypted connection
- Required for sensitive data
- Use platforms like Render, Railway, etc.

---

## 🛠️ If Still Having Issues

### Try These:

1. **Clear Browser Cache**
   ```
   Chrome: Ctrl+Shift+Delete
   Firefox: Ctrl+Shift+Delete
   Safari: Cmd+Opt+E
   ```

2. **Use Incognito/Private Mode**
   - Opens fresh session without cached redirects

3. **Try Different Browser**
   - Chrome usually works best
   - Avoid browsers with strict security extensions

4. **Check Firewall**
   ```bash
   # Windows: Allow port 8000
   New-NetFirewallRule -DisplayName "Django Dev" -Direction Inbound -LocalPort 8000 -Protocol TCP -Action Allow
   ```

5. **Restart Server**
   ```bash
   # Stop current server (Ctrl+C)
   python manage.py runserver 0.0.0.0:8000
   ```

---

## 🎯 Quick Test

### Test from Desktop:
Open browser: `http://localhost:8000`
Should work immediately ✅

### Test from Mobile:
1. Get your IP: `ipconfig` → `192.168.x.x`
2. Open mobile browser
3. Go to: `http://YOUR_IP:8000`
4. Should see login page ✅

---

## 📊 Common Scenarios

### Scenario 1: Desktop Testing
```
URL: http://localhost:8000
Status: ✅ Works
Note: Fastest, no network needed
```

### Scenario 2: Mobile on Same WiFi
```
URL: http://192.168.1.100:8000
Status: ✅ Works
Note: Both devices must be on same WiFi network
```

### Scenario 3: Mobile on Different Network
```
Option A: ngrok
URL: https://abc123.ngrok.io
Status: ✅ Works from anywhere

Option B: Port Forwarding
URL: http://YOUR_PUBLIC_IP:8000
Status: ⚠️ Requires router configuration
```

---

## 💡 Pro Tips

1. **Always use http:// for development**
   - Never https:// with Django dev server

2. **Bookmark the correct URL**
   - Save `http://YOUR_IP:8000` in mobile bookmarks

3. **Disable auto-HTTPS extensions temporarily**
   - Turn off "HTTPS Everywhere" while testing

4. **Use Chrome for testing**
   - Best compatibility with dev server
   - Good developer tools

5. **Keep server running**
   - Don't close terminal while testing
   - Server must stay active

---

## 🆘 Still Not Working?

### Check This Checklist:

- [ ] Server is running (`python manage.py runserver 0.0.0.0:8000`)
- [ ] Using `http://` not `https://`
- [ ] Including port `:8000`
- [ ] Mobile and computer on same WiFi
- [ ] Firewall allows port 8000
- [ ] Correct IP address used
- [ ] Browser cache cleared

### If All Else Fails:

1. **Test on desktop first:**
   ```
   http://localhost:8000
   ```

2. **If desktop works but mobile doesn't:**
   - Check IP address
   - Check firewall
   - Check WiFi network

3. **If nothing works:**
   - Restart server
   - Restart computer
   - Try different device/browser

---

## ✅ Summary

**The Fix:**
- Use `http://` instead of `https://`
- Server is already configured correctly
- Access via: `http://YOUR_IP:8000`

**Why:**
- Django dev server only supports HTTP
- HTTPS requires production WSGI/ASGI server
- For production deployment, use platforms with SSL

**For Now:**
- Continue using HTTP for development
- Switch to HTTPS only when deploying to production

---

**Your server is running correctly now!** Just remember to always use `http://` 🎉
