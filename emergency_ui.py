import cv2


# =====================================
# SOS COUNTDOWN
# =====================================

def draw_sos_countdown(frame, countdown):

    cv2.putText(
        frame,
        f"Sending SOS in {countdown}",
        (120, 330),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 0, 255),
        3
    )

    cv2.putText(
        frame,
        "Press C to Cancel",
        (150, 380),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2
    )


# =====================================
# SOS SENT
# =====================================

def draw_sos_sent(frame):

    cv2.putText(
        frame,
        "SOS SENT SUCCESSFULLY",
        (70, 350),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 0, 255),
        3
    )