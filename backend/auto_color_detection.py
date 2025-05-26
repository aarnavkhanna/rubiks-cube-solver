import cv2
import numpy as np
import os
from utils.color_classifier import classify_color

def process_face_image(image_path):
    img = cv2.imread(image_path)
    img = cv2.resize(img, (600, 600))
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    colors = []
    step = 200 // 3
    offset = 200

    for row in range(3):
        for col in range(3):
            x = offset + col * step + step // 2
            y = offset + row * step + step // 2
            h, s, v = hsv[y, x]
            colors.append(classify_color(h, s, v))

    return colors

def get_cube_state_from_faces():
    faces_dir = "extracted_faces"
    face_order = ['U', 'R', 'F', 'D', 'L', 'B']
    face_files = sorted(os.listdir(faces_dir))[:6]

    cube_state = ''
    for img in face_files:
        face_colors = process_face_image(os.path.join(faces_dir, img))
        cube_state += ''.join(face_colors)

    print("Cube string:", cube_state)
    return cube_state
