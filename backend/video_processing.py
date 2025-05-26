import cv2
import os

def extract_6_faces(video_path):
    video_cap = cv2.VideoCapture(video_path)
    frames_dir = "extracted_faces"
    os.makedirs(frames_dir, exist_ok=True)

    count = 0
    saved = 0
    max_faces = 6

    while True:
        success, frame = video_cap.read()
        if not success or saved == max_faces:
            break
        if count % 60 == 0:
            cv2.imwrite(f"{frames_dir}/face_{saved}.jpg", frame)
            saved += 1
        count += 1

    video_cap.release()
