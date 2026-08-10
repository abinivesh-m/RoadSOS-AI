import cv2

# =====================================
# LOAD FACE DETECTOR
# =====================================

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# =====================================
# LOAD EYE DETECTOR
# =====================================

eye_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_eye.xml"
)

# =====================================
# GLOBAL COUNTER
# =====================================

closed_eyes_frames = 0

# =====================================
# DROWSINESS DETECTION FUNCTION
# =====================================

def detect_drowsiness(frame):

    global closed_eyes_frames

    drowsy = False

    face_detected = False

    # =====================================
    # CONVERT TO GRAYSCALE
    # =====================================

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # =====================================
    # FACE DETECTION
    # =====================================

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=5
    )

    # =====================================
    # PROCESS FACES
    # =====================================

    for (x, y, w, h) in faces:

        face_detected = True

        # Draw face rectangle
        cv2.rectangle(
    frame,
    (x + 40, y + 40),
    (x + w - 40, y + h - 40),
    (255, 0, 0),
    1
)

        # =====================================
        # EYE REGION
        # =====================================

        roi_gray = gray[y + h//4:y + h//2, x:x+w]

        roi_color = frame[y + h//4:y + h//2, x:x+w]

        # =====================================
        # DETECT EYES
        # =====================================

        eyes = eye_cascade.detectMultiScale(
            roi_gray,
            scaleFactor=1.1,
            minNeighbors=10,
            minSize=(30, 30)
        )

        # =====================================
        # EYE LOGIC
        # =====================================

        if len(eyes) >= 2:

            # Reduce counter smoothly
            closed_eyes_frames = max(
                0,
                closed_eyes_frames - 2
            )

            # Draw eye rectangles
            for (ex, ey, ew, eh) in eyes:

                cv2.rectangle(
                    roi_color,
                    (ex, ey),
                    (ex + ew, ey + eh),
                    (0, 255, 0),
                    2
                )

        else:

            # Slow increase
            closed_eyes_frames += 0.2

    # =====================================
    # RESET IF NO FACE
    # =====================================

    if not face_detected:

        closed_eyes_frames = 0

    # =====================================
    # SHOW COUNTER
    # =====================================

    cv2.putText(
        frame,
        f"Closed Frames: {int(closed_eyes_frames)}",
        (50, 150),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 0),
        2
    )

    # =====================================
    # DROWSINESS ALERT
    # =====================================

    if closed_eyes_frames > 15:
        drowsy = True
    return frame, drowsy