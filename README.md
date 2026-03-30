# Helmet-Numberplate-Speed Detection System 🚨

Advanced real-time traffic violation monitoring system with automated helmet detection, license plate recognition, and overspeeding alerts.

## 🚀 How to Start (Quick Launch)

To enable **Real-Time Alerts** (Vibration & Sound) on mobile devices, use the following two-step startup:

### Step 1: Start the Server (Terminal 1)
```bash
uvicorn mini.asgi:application --host 0.0.0.0 --port 8000 --reload
```

### Step 2: Quick Mobile Connection (Terminal 2)
```bash
python scripts/show_qr.py
```
**Scan the QR code** that appears in your terminal with your phone's camera to instantly open the Dashboard.

## 📱 Mobile Alert Activation
Due to mobile browser security (iPhone & Android), you **must tap the screen** once after the dashboard loads to "arm" the system:
1.  **Refresh the page** on your phone.
2.  Tap on the **Red Activation Overlay** (it pulses for visibility).
3.  Your phone is now ready to vibrate and play siren sounds for any detected violations!

## 📁 Project Structure
- `app/`: Main Django application (Logic, Templates, Static).
- `mini/`: Project configuration (Settings, Routing, ASGI).
- `docs/`: Technical summaries and user guides.
- `scripts/`: Helper scripts for IP detection, QR generation, and database management.
- `media/`: Storage for violation captures and test videos.
- `predictspeed.py`: Core AI engine for speed calculation.

## 🛠️ Technology Stack
- **AI Models**: YOLOv7, YOLOv8, YOLOv9.
- **Tracking**: DeepSORT for speed measurement.
- **OCR**: Tesseract/EasyOCR for plate recognition.
- **Backend**: Django 5.0 + Channels (WebSockets).
- **Frontend**: Vanilla JS with Luxury Dark Theme.

## 🔧 One-Time Installation
```bash
pip install -r requirements.txt
pip install uvicorn[standard] daphne qrcode
```

---
*Developed for advanced traffic safety monitoring.*
