import cv2
import mediapipe as mp
from scipy.spatial import distance

# =====================================
# MEDIAPIPE FACE MESH
# =====================================

mp_face_mesh = mp.solutions.face_mesh

face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# =====================================
# EYE LANDMARKS
# =====================================

LEFT_EYE = [362, 385, 387, 263, 373, 380]

RIGHT_EYE = [33, 160, 158, 133, 153, 144]

# =====================================
# DROWSINESS VARIABLES
# =====================================

closed_frames = 0

EAR_THRESHOLD = 0.20

DROWSY_FRAMES = 30

# =====================================
# EAR FUNCTION
# =====================================

def calculate_ear(eye_points):

    vertical_1 = distance.euclidean(
        eye_points[1],
        eye_points[5]
    )

    vertical_2 = distance.euclidean(
        eye_points[2],
        eye_points[4]
    )

    horizontal = distance.euclidean(
        eye_points[0],
        eye_points[3]
    )

    ear = (
        vertical_1 + vertical_2
    ) / (2.0 * horizontal)

    return ear

# =====================================
# DROWSINESS DETECTION
# =====================================

def detect_drowsiness(frame):

    global closed_frames

    drowsy = False

    rgb_frame = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )

    results = face_mesh.process(rgb_frame)

    if results.multi_face_landmarks:

        for face_landmarks in results.multi_face_landmarks:

            h, w, _ = frame.shape

            left_eye_points = []

            right_eye_points = []

            # =====================================
            # LEFT EYE
            # =====================================

            for idx in LEFT_EYE:

                x = int(
                    face_landmarks.landmark[idx].x * w
                )

                y = int(
                    face_landmarks.landmark[idx].y * h
                )

                left_eye_points.append((x, y))

                cv2.circle(
                    frame,
                    (x, y),
                    1,
                    (0, 255, 0),
                    -1
                )

            # =====================================
            # RIGHT EYE
            # =====================================

            for idx in RIGHT_EYE:

                x = int(
                    face_landmarks.landmark[idx].x * w
                )

                y = int(
                    face_landmarks.landmark[idx].y * h
                )

                right_eye_points.append((x, y))

                cv2.circle(
                    frame,
                    (x, y),
                    1,
                    (0, 255, 0),
                    -1
                )

            # =====================================
            # EAR CALCULATION
            # =====================================

            left_ear = calculate_ear(
                left_eye_points
            )

            right_ear = calculate_ear(
                right_eye_points
            )

            avg_ear = (
                left_ear + right_ear
            ) / 2.0

            # =====================================
            # STORE EAR
            # =====================================

            detect_drowsiness.last_ear = avg_ear

            # =====================================
            # DROWSINESS LOGIC
            # =====================================

            if avg_ear < EAR_THRESHOLD:

                closed_frames += 1

            else:

                closed_frames = max(
                    0,
                    closed_frames - 1
                )

            # =====================================
            # STORE CLOSED FRAMES
            # =====================================

            detect_drowsiness.closed_frames = closed_frames

            # =====================================
            # DROWSY CONDITION
            # =====================================

            if closed_frames > DROWSY_FRAMES:

                drowsy = True

    return frame, drowsy

# =====================================
# EXPOSE VARIABLES
# =====================================

detect_drowsiness.last_ear = 0

detect_drowsiness.closed_frames = 0