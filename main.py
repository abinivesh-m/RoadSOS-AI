import cv2
import time
from emergency.accident_detector import AccidentManager
from alerts.audio_manager import speak_async
from emergency.sos_manager import SOSManager
from utils.analytics_manager import increment
from emergency.gps_manager import GPSManager
from utils.logger import log_event
from utils.camera import start_camera
from ui.dashboard import (
    draw_top_bar,
    draw_title,
    draw_fps,
    draw_speed,
    draw_bottom_panel,
    draw_ear,
    draw_status,
    draw_accident_confidence
)
from ui.emergency_ui import (
    draw_sos_countdown,
    draw_sos_sent
)

from ui.alerts_ui import (
    get_alert_message
)
from detection.phone_detection import detect_phone
from detection.drowsiness_mediapipe import detect_drowsiness
from utils.status_manager import get_status
from utils.risk_engine import calculate_risk_score
from ui.dashboard import draw_risk_score
# =====================================
# START CAMERA
# =====================================

cap = start_camera()
speak_async(
    "Road Safety System Ready"
)
accident_manager = AccidentManager()
sos_manager = SOSManager()
gps_manager = GPSManager()
# =====================================
# FPS VARIABLES
# =====================================

prev_time = time.time()
fps = 0

# =====================================
# ALERT COOLDOWN VARIABLES
# =====================================

phone_alert_timer = 0
drowsy_alert_timer = 0
accident_voice_played = False
sos_voice_played = False
# =====================================
# SPEED VARIABLES
# =====================================

speed = 0


# =====================================
# MAIN LOOP
# =====================================

while True:

    ret, frame = cap.read()

    if not ret:
        break

    # =====================================
    # RESIZE FRAME
    # =====================================

    frame = cv2.resize(frame, (640, 480))

    # =====================================
    # KEYBOARD INPUT
    # =====================================

    key = cv2.waitKey(1) & 0xFF

    # =====================================
    # SPEED CONTROLS
    # =====================================

    if key == ord('w'):

        speed += 2

    if key == ord('s'):

        speed -= 2

    if speed < 0:

        speed = 0

    # =====================================
    # ACCIDENT SIMULATION
    # =====================================
    if key == ord('x'):
         
         accident_manager.trigger_accident()
         if not accident_voice_played:
          log_event(
    "SOS Sent"
)
          increment(
    "accidents"
)                  
          speak_async(
            "Accident detected. Sending emergency SOS."
        )

          accident_voice_played = True
    # =====================================
    # CANCEL SOS
    # =====================================

    if key == ord('c'):

        accident_manager.cancel_accident()

    # =====================================
    # PHONE DETECTION
    # =====================================

    frame, phone_alert = detect_phone(frame)

    # =====================================
    # DROWSINESS DETECTION
    # =====================================

    frame, drowsy = detect_drowsiness(frame)

    # =====================================
    # ALERT COOLDOWN
    # =====================================

    if phone_alert:

     if phone_alert_timer == 0:
        log_event(
    "Phone Usage Detected"
)
        increment(
            "phone_detections"
        )

        speak_async(
            "Mobile usage detected.Focus on the road"
        )

        phone_alert_timer = 150

    if drowsy:

     if drowsy_alert_timer == 0:
        log_event(
    "Drowsiness Detected"
)
        increment(
    "drowsiness_detections"
)
        speak_async(
             "Drowsiness detected. Please take a break."
         )

        drowsy_alert_timer = 150

    if phone_alert_timer > 0:

        phone_alert_timer -= 1

    if drowsy_alert_timer > 0:

        drowsy_alert_timer -= 1

    
    risk_score = calculate_risk_score(
    phone_alert_timer,
    drowsy_alert_timer,
    speed
)
    draw_risk_score(
    frame,
    risk_score
)
    # =====================================
    # REAL SOS TIMER
    # =====================================

    accident_manager.update()
    if not accident_manager.is_accident():
     sos_voice_played = False
     accident_voice_played = False
    sos_manager.update(accident_manager)
    if accident_manager.is_sos_sent():

     sos_manager.send_sos(
        gps_manager
    )

     if not sos_voice_played:

         speak_async(
            "Emergency contacts have been notified."
        )

         sos_voice_played = True
    # =====================================
    # FPS CALCULATION
    # =====================================

    current_time = time.time()

    new_fps = 1 / (current_time - prev_time)

    prev_time = current_time

    fps = (fps * 0.9) + (new_fps * 0.1)

    # =====================================
    # TOP GLASS BAR
    # =====================================

    draw_top_bar(frame)
    # =====================================
    # TITLE
    # =====================================

    draw_title(frame)
    # =====================================
    # FPS DISPLAY
    # =====================================

    draw_fps(frame, fps)

    # =====================================
    # SPEED DISPLAY
    # =====================================

    draw_speed(frame, speed)

    # =====================================
    # EAR DISPLAY
    # =====================================

    draw_ear(
    frame,
    detect_drowsiness.last_ear
)
    draw_accident_confidence(
    frame,
    accident_manager.get_confidence()
)
    # =====================================
    # SYSTEM STATUS
    # =====================================
    status, status_color = get_status(
    phone_alert_timer,
    drowsy_alert_timer,
    speed,
    accident_manager
)
    if speed > 80:

     increment(
        "overspeed_events"
    )
    # =====================================
    # ACCIDENT STATUS
    # =====================================

    if (
        accident_manager.is_accident()
        or accident_manager.is_sos_sent()
    ):

        status = "ACCIDENT"
        status_color = (0, 0, 255)

    draw_status(
        frame,
        status,
        status_color
    )

    # =====================================
    # ALERT MESSAGE
    # =====================================

    alert_message, alert_color = get_alert_message(
        phone_alert_timer,
        drowsy_alert_timer,
        speed,
        accident_manager
    )

    draw_bottom_panel(
        frame,
        alert_message,
        alert_color
    )

    # =====================================
    # SOS COUNTDOWN
    # =====================================

    if (
        accident_manager.is_accident()
        and not accident_manager.is_sos_sent()
    ):

        draw_sos_countdown(
            frame,
            accident_manager.get_countdown()
        )

    # =====================================
    # SOS SENT
    # =====================================

    if accident_manager.is_sos_sent():

        draw_sos_sent(frame)
    # =====================================
    # SHOW OUTPUT
    # =====================================

    cv2.imshow(
        "RoadSOS AI",
        frame
    )

    # =====================================
    # EXIT
    # =====================================

    if key == ord('q'):

        break

# =====================================
# RELEASE
# =====================================

cap.release()
cv2.destroyAllWindows()