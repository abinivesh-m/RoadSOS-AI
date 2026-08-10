from ultralytics import YOLO
import cv2

# =====================================
# LOAD YOLO MODEL
# =====================================

model = YOLO("yolov8n.pt")

# =====================================
# GLOBAL COUNTER
# =====================================

phone_frames = 0

# =====================================
# PHONE DETECTION FUNCTION
# =====================================

def detect_phone(frame):

    global phone_frames

    phone_alert = False

    phone_detected = False

    # =====================================
    # RUN YOLO
    # =====================================

    results = model(
        frame,
        conf=0.4,
        imgsz=224,
        verbose=False
    )

    # =====================================
    # PROCESS RESULTS
    # =====================================

    for result in results:

        boxes = result.boxes

        for box in boxes:

            class_id = int(box.cls[0])

            class_name = model.names[class_id]

            # =====================================
            # CELL PHONE DETECTION
            # =====================================

            if class_name == "cell phone":

                phone_detected = True

                # =====================================
                # CONFIDENCE SCORE
                # =====================================

                confidence = float(box.conf[0])

                confidence_text = f"{confidence:.2f}"

                # =====================================
                # BOX COORDINATES
                # =====================================

                x1, y1, x2, y2 = map(
                    int,
                    box.xyxy[0]
                )

                # =====================================
                # DRAW BOUNDING BOX
                # =====================================

                cv2.rectangle(
                    frame,
                    (x1, y1),
                    (x2, y2),
                    (0, 255, 255),
                    2
                )

                # =====================================
                # LABEL
                # =====================================

                label = f"MOBILE IN USE | {confidence_text}"

                cv2.putText(
                    frame,
                    label,
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 255, 255),
                    2
                )

    # =====================================
    # COUNTER LOGIC
    # =====================================

    if phone_detected:

        phone_frames += 0.2

    else:

        phone_frames = max(
            0,
            phone_frames - 0.1
        )



    # =====================================
    # ALERT CONDITION
    # =====================================

    if phone_frames > 5:

        phone_alert = True

    return frame, phone_alert