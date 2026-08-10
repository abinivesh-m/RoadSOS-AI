# RoadSOS AI

An AI-based driver monitoring and emergency-response prototype that combines phone-usage detection, drowsiness detection, and a simulated accident/SOS pipeline in one real-time dashboard.

**Status:** Software-only prototype, runs on a laptop with a USB webcam. Accident detection and vehicle speed are currently **simulated**, not sensor-driven — see [Current Limitations](#current-limitations) below.

---

## What it does

RoadSOS AI watches the driver through a webcam and tracks two risk factors in real time:

- **Phone usage detection** — YOLOv8 object detection flags when a cell phone is visible/in use.
- **Drowsiness detection** — MediaPipe Face Mesh calculates Eye Aspect Ratio (EAR) to detect prolonged eye closure.

These feed into a **risk engine** that produces a live risk score, shown on an OpenCV dashboard along with voice alerts and event logging.

If an accident is flagged (currently simulated), the system starts an SOS countdown with GPS location, giving the driver a **cancel window** before an emergency notification is sent — reducing the chance of false alarms.

---

## Architecture

```
Camera Input → OpenCV Processing
        ├── YOLO Object Detection → Mobile Phone Usage
        └── MediaPipe Facial Landmarks → Drowsiness / EAR
                ↓
        Risk Engine → Real-Time Risk Score
                ↓
    ┌───────────┼───────────────┐
Dashboard   Voice Alerts   Event Logging
(OpenCV UI) (Async Audio)  / Analytics
                ↓
Accident Event (SIMULATED) → SOS Manager → GPS Manager
                ↓
Emergency Notification (cancel window available before SOS is sent)
```

---

## Project structure

```
RoadSOS-AI/
├── main.py                   # Entry point — runs the camera loop and ties everything together
├── camera.py                 # Webcam capture handling
├── drowsiness_mediapipe.py   # EAR-based drowsiness detection (MediaPipe)
├── drowsiness.py             # Haar-cascade fallback drowsiness detection (OpenCV)
├── phone_detection.py        # YOLOv8 phone-usage detection
├── risk_engine.py            # Combines detections into a real-time risk score
├── accident_detector.py      # Accident trigger + countdown logic (simulated)
├── sos_manager.py            # SOS status + emergency message generation
├── gps_manager.py            # GPS location + Google Maps link
├── audio_manager.py          # Async voice alerts (pyttsx3)
├── dashboard.py              # OpenCV dashboard overlay (speed, risk score, EAR, etc.)
├── alerts_ui.py              # Alert message + color logic
├── emergency_ui.py           # SOS countdown / SOS-sent overlay
├── analytics_manager.py      # Event analytics tracking
├── status_manager.py         # Overall system status tracking
├── logger.py                 # Event logging
├── __init__.py
└── requirements.txt
```

---

## Tech stack

- **OpenCV** — video capture, frame processing, dashboard UI
- **YOLOv8 (Ultralytics)** — phone detection
- **MediaPipe** — facial landmark detection for EAR calculation
- **pyttsx3** — offline text-to-speech voice alerts
- **SciPy** — EAR distance calculations

---

## Running it locally

```bash
pip install -r requirements.txt
python main.py
```

*(Requires a webcam. Press `C` to cancel an active SOS countdown.)*

---

## Current Limitations

This is a hackathon prototype. To keep the demo honest:

- **Accident detection is simulated** — the confidence score (impact + tilt + no-movement) is not yet driven by real accelerometer/gyroscope hardware.
- **Vehicle speed is simulated** via keyboard input (W/S), not a real GPS/OBD feed.
- **GPS/GSM modules** exist in code (`gps_manager.py`, planned SIM800L integration) but aren't wired to physical hardware yet.
- Not yet validated against real-world crash data.

## Future Scope

**Phase 1 — Hardware Integration**
ESP32 + MPU6050 for real crash detection, real GPS tracking, GSM/SMS alerts, real vehicle speed input.

**Phase 2 — Intelligence**
Near-miss detection, personalized AI-driven driver risk modelling over time.

**Phase 3 — Scale**
Companion mobile app, fleet management dashboard, real-world validation with crash data.

---
