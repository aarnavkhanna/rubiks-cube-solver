import cv2
import numpy as np
from skimage import color
import json

face_order = ['U', 'R', 'F', 'D', 'L', 'B']

def preprocess_image(image):
    image = cv2.resize(image, (400, 400))
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    blurred = cv2.GaussianBlur(hsv, (5, 5), 0)
    return blurred

def get_center_lab(image_path):
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Failed to load {image_path}")
    image = preprocess_image(image)

    step = image.shape[0] // 3
    y = x = step + step // 2  # center patch
    patch_size = step // 4

    patch = image[y - patch_size:y + patch_size, x - patch_size:x + patch_size]
    avg_bgr = np.mean(patch, axis=(0, 1)).astype(np.uint8)
    avg_rgb = cv2.cvtColor(np.uint8([[avg_bgr]]), cv2.COLOR_HSV2RGB)[0][0]

    lab = color.rgb2lab(np.array([[avg_rgb]], dtype=np.uint8))[0][0]
    return lab.tolist()

def calibrate_cube(image_paths):
    lab_profile = {}
    for face, path in zip(face_order, image_paths):
        lab = get_center_lab(path)
        lab_profile[face] = lab
        print(f"✅ {face} center LAB:", lab)

    with open("cube_profile.json", "w") as f:
        json.dump(lab_profile, f, indent=2)
    print("🎯 Calibration complete. Profile saved to cube_profile.json")

if __name__ == "__main__":
    image_paths = [
        "uploads/face1.jpg",  # U
        "uploads/face2.jpg",  # R
        "uploads/face3.jpg",  # F
        "uploads/face4.jpg",  # D
        "uploads/face5.jpg",  # L
        "uploads/face6.jpg",  # B
    ]
    calibrate_cube(image_paths)
