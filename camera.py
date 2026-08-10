import cv2

def start_camera(camera_index=0):

    cap = cv2.VideoCapture(camera_index)

    # Lower resolution for better FPS
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    if not cap.isOpened():

        print("Error: Cannot access camera")
        exit()

    return cap