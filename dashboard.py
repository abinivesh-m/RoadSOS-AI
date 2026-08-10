import cv2
def draw_status(frame, status, status_color):

    cv2.putText(
        frame,
        status,
        (470, 42),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.9,
        status_color,
        2
    )

# =====================================
# TOP GLASS BAR
# =====================================

def draw_top_bar(frame):

    overlay = frame.copy()

    cv2.rectangle(
        overlay,
        (0, 0),
        (640, 70),
        (15, 15, 15),
        -1
    )

    cv2.addWeighted(
        overlay,
        0.7,
        frame,
        0.3,
        0,
        frame
    )


# =====================================
# TITLE
# =====================================

def draw_title(frame):

    cv2.putText(
        frame,
        "RoadSOS AI",
        (20, 42),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 255, 255),
        2
    )

# =====================================
# FPS
# =====================================

def draw_fps(frame, fps):

    cv2.putText(
        frame,
        f"FPS: {int(fps)}",
        (20, 100),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 0),
        2
    )


# =====================================
# SPEED
# =====================================

def draw_speed(frame, speed):

    color = (0, 255, 0)

    if speed > 60:

        color = (0, 255, 255)

    if speed > 80:
    
    
      color = (0, 0, 255)

    cv2.putText(
        frame,
        f"Speed: {speed} km/h",
        (20, 140),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        color,
        2
    )


# =====================================
# BOTTOM PANEL
# =====================================

def draw_bottom_panel(
        frame,
        message,
        color
):

    overlay = frame.copy()

    cv2.rectangle(
        overlay,
        (0, 430),
        (640, 480),
        (15, 15, 15),
        -1
    )

    cv2.addWeighted(
        overlay,
        0.7,
        frame,
        0.3,
        0,
        frame
    )

    cv2.putText(
        frame,
        message,
        (20, 458),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        color,
        2
    )


# =====================================
# EAR DISPLAY
# =====================================

def draw_ear(frame, ear):

    cv2.putText(
        frame,
        f"EAR: {ear:.2f}",
        (20, 180),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2
    )
    
    # =====================================
# RISK SCORE
# =====================================

def draw_risk_score(frame, risk_score):

    color = (0, 255, 0)

    if risk_score >= 40:
        color = (0, 255, 255)

    if risk_score >= 70:
        color = (0, 0, 255)

    cv2.putText(
        frame,
        f"Risk Score: {risk_score}/100",
        (20, 220),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        color,
        2
    )


def draw_accident_confidence(frame, confidence):

    color = (0, 255, 0)

    if confidence >= 40:
        color = (0, 255, 255)

    if confidence >= 70:
        color = (0, 0, 255)

    cv2.putText(
        frame,
        f"Accident Confidence: {confidence}%",
        (20, 260),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        color,
        2
    )