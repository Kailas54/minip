# 🌐 Server Access - Quick Reference

## ✅ Your Server is Running!

**Current Status:**
```
✅ Running at: http://0.0.0.0:8000
✅ Protocol: HTTP only
✅ Accessible from: All devices on same network
```

---

## 🔗 Access URLs

### From Desktop:
```
http://localhost:8000
```

### From Mobile (Same WiFi):
```
http://YOUR_IP:8000
```
Example: `http://192.168.1.100:8000`

### Find Your IP (Windows):
```bash
ipconfig
```

---

## ⚠️ IMPORTANT

### DO's:
✅ Use `http://` (with single 's')  
✅ Include port `:8000`  
✅ Keep server running  
✅ Use on trusted networks  

### DON'Ts:
❌ Don't use `https://` (no 's'!)  
❌ Don't expose to public internet  
❌ Don't use for production  
❌ Don't share public IP  

---

## 🚀 Quick Start

1. **Server running?** ✓
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```

2. **Find your IP:**
   ```bash
   ipconfig → 192.168.x.x
   ```

3. **Open on mobile:**
   ```
   http://192.168.x.x:8000
   ```

4. **Login:**
   - License Number
   - Phone Number

---

## 🔧 Common Issues

| Issue | Solution |
|-------|----------|
| HTTPS error | Use `http://` not `https://` |
| Can't connect | Check firewall allows port 8000 |
| Wrong IP | Run `ipconfig` again |
| Page won't load | Clear browser cache |

---

## 📱 Mobile Testing

**Best Practice:**
1. Use Chrome on Android
2. Bookmark the URL
3. Disable HTTPS extensions
4. Stay on same WiFi network

---

## 💡 Remember

- Development server = HTTP only
- Production hosting = HTTPS required
- For now: Stick with HTTP!

**Server is ready! Just use http://** ✅
