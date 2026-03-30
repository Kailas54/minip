# 📳 WebSocket Vibration Notification System

## 🎯 Overview

This system provides **real-time haptic feedback** to mobile browsers when traffic violations are detected, without requiring a native mobile app. It uses the **HTML5 Vibration API** combined with **WebSocket technology** for instant push notifications.

---

## 🔧 Architecture

### Three-Layer System

```
┌─────────────────────────────────────────────────────────────┐
│  Detection Layer (Backend - Python/Django)                  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ YOLOv8 detects violation → Triggers WebSocket event  │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  Communication Layer (WebSocket - Real-time)                │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Django Channels pushes notification to specific user │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  Execution Layer (Frontend - JavaScript/Mobile Browser)     │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ navigator.vibrate(pattern) → Physical vibration!     │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## 📂 Files Added/Modified

### New Files Created:

1. **`app/websocket_consumer.py`**
   - WebSocket consumer classes
   - Handles real-time communication
   - Generates vibration patterns

2. **`app/routing.py`**
   - WebSocket URL routing
   - Maps URLs to consumers

3. **`WEBSOCKET_VIBRATION_GUIDE.md`** (this file)
   - Complete documentation

### Modified Files:

1. **`mini/settings.py`**
   - Added `channels` to INSTALLED_APPS
   - Configured ASGI application
   - Set up channel layers

2. **`mini/asgi.py`**
   - Wrapped with WebSocket support
   - Protocol router configuration

3. **`app/views.py`**
   - Integrated WebSocket notifications
   - Sends vibration alerts on violations

4. **`app/templates/app/user_dashboard.html`**
   - Client-side WebSocket connection
   - Vibration API implementation
   - Visual notifications

5. **`requirements.txt`**
   - Added channels packages

---

## 🔍 How It Works

### Step 1: User Opens Dashboard on Mobile

```javascript
// When user loads user_dashboard.html
const userPhone = '{{ user_phone }}'; // e.g., "9876543210"

// WebSocket connection established automatically
ws://192.168.1.100:8000/ws/notifications/9876543210/
```

### Step 2: Violation Detected by YOLOv8

```python
# In production_processor.py or process_video()
violating_plates = ['DL01AB1234', 'MH02CD5678']

# For each violating plate, check if registered
for plate in violating_plates:
    registered_user = RegisteredUser.objects.get(vehicle_number=plate)
    
    # Send WebSocket notification
    channel_layer.group_send(
        f'vibration_{registered_user.phone_number}',
        {
            'type': 'send_vibration_alert',
            'violation_type': 'no_helmet',
            'plate_number': plate,
            'severity': 'high',
            'vibration_pattern': [500, 200, 500, 200, 500]
        }
    )
```

### Step 3: Mobile Receives Notification

```javascript
// WebSocket message received
{
    "type": "vibration_alert",
    "violation_type": "no_helmet",
    "plate_number": "DL01AB1234",
    "severity": "high",
    "vibration_pattern": [500, 200, 500, 200, 500],
    "message": "No Helmet Detected for vehicle DL01AB1234"
}

// Execute vibration
navigator.vibrate([500, 200, 500, 200, 500]);
// Phone vibrates: 500ms ON, 200ms OFF, 500ms ON, 200ms OFF, 500ms ON
```

---

## 📱 Vibration Patterns

### Pattern Format
Array of milliseconds: `[on, off, on, off, ...]`

### Severity-Based Patterns

| Severity | Pattern | Description |
|----------|---------|-------------|
| **LOW** | `[300]` | Single short buzz (300ms) |
| **MEDIUM** | `[400, 200, 400]` | Two medium pulses |
| **HIGH** | `[500, 200, 500, 200, 500]` | Triple long vibration |

### Violation-Type Patterns

```python
def get_vibration_pattern(severity, violation_type):
    if severity == 'high':
        return [500, 200, 500, 200, 500]  # Strong alert
    elif severity == 'medium':
        return [400, 200, 400]             # Medium alert
    else:
        return [300]                        # Gentle alert
```

---

## 🔐 Security & Permissions

### Browser Security Requirements

1. **User Gesture Required**
   - Vibration API requires user interaction first
   - Solution: Enable on first click/tap anywhere on page

2. **HTTPS for Production**
   - Some browsers require secure context
   - Use `wss://` instead of `ws://` in production

3. **Permission Request**
   ```javascript
   async function requestVibrationPermission() {
       const result = await navigator.permissions.query({ name: 'vibrate' });
       return result.state === 'granted';
   }
   ```

### Implementation

```javascript
// Wait for first user interaction
document.body.addEventListener('click', function requestPermission() {
    requestVibrationPermission().then(function(granted) {
        if (granted) {
            vibrationEnabled = true;
            connectWebSocket();
        }
    });
    document.body.removeEventListener('click', requestPermission);
}, { once: true });
```

---

## 🌐 Network Configuration

### Development (Local Network)

```bash
# Server runs on your computer
python manage.py runserver 0.0.0.0:8000

# Mobile connects via WiFi
ws://192.168.1.100:8000/ws/notifications/PHONE_NUMBER/
```

### Production (Internet)

```bash
# With ngrok
ngrok http 8000

# Mobile connects via
wss://abc123.ngrok.io/ws/notifications/PHONE_NUMBER/
```

### Production (Hosting Platform)

```bash
# Deployed to Render/Railway
wss://yourproject.onrender.com/ws/notifications/PHONE_NUMBER/
```

---

## 🧪 Testing Guide

### Test 1: Basic Vibration

Open browser console and test:
```javascript
// Short vibration
navigator.vibrate(300);

// Pattern vibration
navigator.vibrate([500, 200, 500]);
```

### Test 2: WebSocket Connection

1. Open dashboard on mobile
2. Open browser console (F12)
3. Look for: `Connecting to WebSocket: ws://...`
4. Should see: `WebSocket connected`

### Test 3: Simulate Violation

Open Django shell:
```bash
python manage.py shell
```

```python
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

channel_layer = get_channel_layer()

# Send test vibration to phone number 9876543210
async_to_sync(channel_layer.group_send)(
    'vibration_9876543210',
    {
        'type': 'send_vibration_alert',
        'violation_type': 'overspeeding',
        'plate_number': 'TEST123',
        'speed': '120 km/h',
        'severity': 'high',
        'timestamp': '2024-03-25 10:00:00'
    }
)
```

Your phone should vibrate immediately!

---

## 📊 Browser Compatibility

### Desktop Browsers
❌ **No vibration support** (no hardware)
✅ Notifications still show visually

### Mobile Browsers

| Browser | Vibration Support | Notes |
|---------|------------------|-------|
| **Chrome Android** | ✅ Full support | Best compatibility |
| **Firefox Android** | ✅ Full support | Good alternative |
| **Samsung Internet** | ✅ Full support | Works well |
| **Safari iOS** | ❌ No support | Apple doesn't allow |
| **Opera Android** | ✅ Full support | Chromium-based |

### iOS Workaround

Since Safari iOS doesn't support vibration API:
```javascript
// Fallback to visual notifications only
if (!('vibrate' in navigator)) {
    console.log('Vibration not supported, using visual alerts only');
    showNotification(message, type);
}
```

---

## 🔧 Troubleshooting

### Issue 1: Vibration Not Working

**Check:**
1. ✅ Browser supports vibration API
2. ✅ User has interacted with page (clicked/tapped)
3. ✅ WebSocket connection is open
4. ✅ Phone is not in silent/do-not-disturb mode

**Debug:**
```javascript
console.log('Vibration supported:', 'vibrate' in navigator);
console.log('Vibration enabled:', vibrationEnabled);
console.log('WebSocket state:', vibrationWebSocket?.readyState);
```

### Issue 2: WebSocket Not Connecting

**Check:**
1. ✅ Server is running with Daphne (ASGI server)
2. ✅ Correct IP address/port
3. ✅ Firewall allows WebSocket connections
4. ✅ Routing configuration is correct

**Start ASGI server:**
```bash
# For development with Channels
python -m daphne -b 0.0.0.0 -p 8000 mini.asgi:application

# Or use runserver (automatically uses Daphne with Channels)
python manage.py runserver 0.0.0.0:8000
```

### Issue 3: Notifications Not Appearing

**Check:**
1. ✅ Phone number matches exactly
2. ✅ User is logged in
3. ✅ Vehicle is registered
4. ✅ Violation detection is working

**Test WebSocket directly:**
```bash
# Install wscat
npm install -g wscat

# Connect to WebSocket
wscat -c ws://192.168.1.100:8000/ws/notifications/9876543210/

# Send ping
{"type": "ping", "timestamp": "2024-03-25T10:00:00Z"}
```

---

## 🚀 Deployment Checklist

### Development Setup
- [ ] Install channels packages
- [ ] Configure ASGI application
- [ ] Set up channel layers
- [ ] Test WebSocket connection locally
- [ ] Verify vibration on mobile

### Production Deployment

1. **Update settings.py**
   ```python
   CHANNEL_LAYERS = {
       'default': {
           'BACKEND': 'channels_redis.core.RedisChannelLayer',
           'CONFIG': {
               "hosts": [("redis-server-ip", 6379)],
           },
       }
   }
   ```

2. **Install Redis** (for production)
   ```bash
   sudo apt-get install redis-server
   pip install channels-redis
   ```

3. **Use HTTPS/WSS**
   - SSL certificate required
   - Secure WebSocket connection

4. **Configure firewall**
   - Allow WebSocket port
   - Enable WSS protocol

---

## 📈 Performance Considerations

### Connection Management

```javascript
// Heartbeat to keep connection alive
setInterval(() => {
    if (vibrationWebSocket.readyState === WebSocket.OPEN) {
        vibrationWebSocket.send(JSON.stringify({
            type: 'ping',
            timestamp: new Date().toISOString()
        }));
    }
}, 30000); // Every 30 seconds
```

### Reconnection Logic

```javascript
vibrationWebSocket.onclose = function(event) {
    console.log('WebSocket disconnected');
    vibrationEnabled = false;
    
    // Attempt to reconnect after 5 seconds
    setTimeout(connectWebSocket, 5000);
};
```

### Battery Optimization

- Vibration only when necessary
- Use appropriate patterns (not too long)
- Allow user to disable vibrations
- Auto-disconnect when page hidden

---

## 🎯 User Experience Flow

```
1. User opens dashboard on mobile
         ↓
2. Clicks anywhere on page (grants permission)
         ↓
3. WebSocket connects automatically
         ↓
4. User goes about daily activities
         ↓
5. Violation detected by backend
         ↓
6. WebSocket pushes notification
         ↓
7. Phone vibrates immediately
         ↓
8. Visual toast notification appears
         ↓
9. User sees violation details
```

---

## 🔮 Future Enhancements

### Planned Features:

1. **Customizable Patterns**
   - Let users choose vibration styles
   - Different patterns for different violation types

2. **Sound Alerts**
   - Add optional audio notifications
   - Customizable alert sounds

3. **Notification History**
   - Store received notifications
   - View past alerts

4. **Smart Filtering**
   - Only vibrate for high-severity violations
   - Quiet hours configuration

5. **Multi-Device Support**
   - Connect multiple devices to same account
   - Broadcast to all devices simultaneously

---

## 📞 Support & Resources

### Documentation:
- [Django Channels Docs](https://channels.readthedocs.io/)
- [HTML5 Vibration API](https://developer.mozilla.org/en-US/docs/Web/API/Vibration_API)
- [WebSocket Protocol](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket)

### Testing Tools:
- Browser DevTools (F12)
- wscat (WebSocket CLI client)
- Django Debug Toolbar

### Common Issues:
See Troubleshooting section above

---

## ✅ Summary

You now have a **production-ready WebSocket vibration notification system** that:

✅ Provides instant haptic feedback  
✅ Works on mobile browsers (no app needed)  
✅ Uses standard HTML5 APIs  
✅ Scales with Django Channels  
✅ Respects browser security requirements  
✅ Includes fallback visual notifications  
✅ Supports custom vibration patterns  

**Perfect for academic projects demonstrating real-time mobile notifications!** 🎓📱

---

**Version:** 1.0  
**Last Updated:** March 25, 2026  
**Status:** Production Ready ✅
