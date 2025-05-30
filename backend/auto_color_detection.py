import cv2
import numpy as np
from skimage import color
from collections import Counter
import os
import json

# Load personalized LAB profile generated from calibrate_cube.py
with open("cube_profile.json") as f:
    PROFILE_LAB = json.load(f)

CENTER_LAB_MAP = {face: np.array(lab) for face, lab in PROFILE_LAB.items()}

def preprocess_image(image):
    image = cv2.resize(image, (400, 400))
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    blurred = cv2.GaussianBlur(hsv, (5, 5), 0)
    return blurred

def classify_color(sample_rgb):
    sample_lab = color.rgb2lab(np.array([[sample_rgb]], dtype=np.uint8))[0][0]
    min_dist = float('inf')
    closest_face = None
    for face, center_lab in CENTER_LAB_MAP.items():
        dist = np.linalg.norm(sample_lab - center_lab)
        if dist < min_dist:
            min_dist = dist
            closest_face = face
    return closest_face

def detect_colors(image_path):
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Could not read image at path: {image_path}")

    preprocessed = preprocess_image(image)
    step = preprocessed.shape[0] // 3
    patch_size = step // 4  # average over region

    colors = []
    for row in range(3):
        for col in range(3):
            y = row * step + step // 2
            x = col * step + step // 2
            y1, y2 = y - patch_size, y + patch_size
            x1, x2 = x - patch_size, x + patch_size

            patch = preprocessed[y1:y2, x1:x2]
            avg_bgr = np.mean(patch, axis=(0, 1)).astype(np.uint8)
            avg_rgb = cv2.cvtColor(np.uint8([[avg_bgr]]), cv2.COLOR_HSV2RGB)[0][0]

            label = classify_color(avg_rgb)
            if label is None:
                raise ValueError("Could not classify one of the colors.")
            colors.append(label)
    return colors

def get_cube_state_from_images(image_paths):
    if len(image_paths) != 6:
        raise ValueError("Exactly 6 images required: [U, R, F, D, L, B]")

    face_order = ['U', 'R', 'F', 'D', 'L', 'B']
    cube_string = ""
    detected_faces = []

    for idx, path in enumerate(image_paths):
        face = detect_colors(path)
        print(f"📸 Detected {face_order[idx]} face: {face}")
        detected_faces.append(face)

    print("🎯 Detected cube using personalized LAB profile:", CENTER_LAB_MAP)

    for face in detected_faces:
        for face_label in face:
            cube_string += face_label

    return cube_string
