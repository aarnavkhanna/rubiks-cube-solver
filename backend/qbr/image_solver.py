import cv2
from qbr.colordetection import ColorDetection

def solve_cube_from_images(image_paths):
    if len(image_paths) != 6:
        raise ValueError("Exactly 6 images required in URFDLB order")

    detector = ColorDetection()
    cube_string = ""
    all_bgrs = []
    center_bgrs = {}

    face_order = ['U', 'R', 'F', 'D', 'L', 'B']

    # First pass: collect BGRs and center BGRs
    for face_index, path in enumerate(image_paths):
        img = cv2.imread(path)
        if img is None:
            raise ValueError(f"Failed to read image: {path}")

        h, w, _ = img.shape
        step = w // 3
        offset = h // 3

        for row in range(3):
            for col in range(3):
                x = col * step
                y = row * offset
                roi = img[y:y+offset, x:x+step]
                dominant_bgr = detector.get_dominant_color(roi)
                all_bgrs.append(dominant_bgr)

                # Save center tile's BGR
                if row == 1 and col == 1:
                    center_bgrs[face_order[face_index]] = dominant_bgr

    # Set color palette using center BGRs
    detector.set_palette_by_centers(center_bgrs)

    # Second pass: build the cube string
    for bgr in all_bgrs:
        cube_string += detector.convert_bgr_to_notation(bgr)

    return cube_string
