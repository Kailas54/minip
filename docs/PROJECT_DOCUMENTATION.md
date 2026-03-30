# Helmet, Number Plate, and Speed Detection System

This project is a comprehensive traffic monitoring solution designed to detect safety violations (no-helmet), identify vehicles via number plate extraction, and monitor vehicle speed using computer vision.

## 🚀 Features

- **Real-time Detection**: Uses YOLO (v7, v8, and v9) models for high-accuracy object detection.
- **Helmet Detection**: Identifies motorcyclists riding without helmets.
- **Number Plate Extraction**: Extracts text from vehicle number plates using OCR (Tesseract).
- **Speed Estimation**: Monitors vehicle movement to detect speeding violations.
- **Modern Dashboard**: A clean, responsive web interface built with Django and Bootstrap for uploading footage and visualizing results.

---

## 🛠️ Tech Stack

- **Backend**: Django (Python 3.10+)
- **Frontend**: HTML5, CSS3 (Custom + Bootstrap), JavaScript
- **AI/ML**: YOLOv8 (Ultralytics), YOLOv7, YOLOv9
- **OCR**: Tesseract OCR
- **Dataset Management**: Roboflow
- **Environment**: Google Colab (for training), Local Server (for execution)

---

## 📂 Project Structure

```text
Helmet-Numberplate-Speed-Detection/
├── app/                    # Django application logic
│   ├── static/             # CSS, JS, and Images
│   ├── templates/          # HTML templates (Dashboard, Registration)
│   ├── models.py           # Database schemas
│   └── views.py            # Business logic and routing
├── platevision/            # Django project configuration
├── YOLOv8.ipynb            # Model training & inference notebook for v8
├── YOLOv7.ipynb            # Model training & inference notebook for v7
├── YOLOv9.ipynb            # Model training & inference notebook for v9
├── predictspeed.py         # Speed detection logic
├── Tesseract OCR.py        # License plate extraction logic
├── requirements.txt        # Python dependencies
└── manage.py               # Django management script
```

---

## 🏁 Getting Started

### 1. Prerequisites
- Python 3.10+
- Tesseract OCR installed on your system.
- NVIDIA GPU (Recommended for training).
    
#                 
### 3. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Running the Application
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000/` in your browser.

---

## 🧠 Model Training

The models are trained using **Transfer Learning** on custom datasets downloaded from Roboflow. Detailed steps can be found in the respective `.ipynb` notebooks.

1.  **Environment**: Tesla T4 GPU (Google Colab).
2.  **Dataset**: Helmet and Numberplate detection dataset (YOLO format).
3.  **Process**:
    - Build environment with `ultralytics`.
    - Download weights (e.g., `yolov8s.pt`).
    - Train for 100 epochs using the `train.py` script.
    - Export `best.pt` for deployment.

---

## 📝 Usage

1.  **Upload**: Click the upload icon on the dashboard to select a traffic video (.mp4 or .mov).
2.  **Analyze**:
    - **Detect Helmet**: Checks for riders without safety gear.
    - **Detect Speed**: Visualizes speed zones and flags violations.
    - **Extract Plate**: Performs OCR to read the number plate text.
3.  **Results**: View live results and statistics in the analysis section.

---

## 🤝 Contact
For any queries, please reach out to the project maintainers.
