import numpy as np
import cv2
from .helpers import ciede2000, bgr2lab
from .config import config
from .constants import CUBE_PALETTE, COLOR_PLACEHOLDER

class ColorDetection:
    def __init__(self):
        self.prominent_color_palette = {
            'red'   : (0, 0, 255),
            'orange': (0, 165, 255),
            'blue'  : (255, 0, 0),
            'green' : (0, 255, 0),
            'white' : (255, 255, 255),
            'yellow': (0, 255, 255)
        }

        self.cube_color_palette = config.get_setting(
            CUBE_PALETTE,
            self.prominent_color_palette
        )
        for side, bgr in self.cube_color_palette.items():
            self.cube_color_palette[side] = tuple(bgr)

    def get_dominant_color(self, roi):
        pixels = np.float32(roi.reshape(-1, 3))
        _, labels, palette = cv2.kmeans(pixels, 1, None,
                                        (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, 0.1),
                                        10, cv2.KMEANS_RANDOM_CENTERS)
        return tuple(palette[0])

    def convert_bgr_to_notation(self, bgr):
        if not hasattr(self, 'dynamic_palette'):
            raise ValueError("Dynamic palette not set. Run set_palette_by_centers() first.")

        distances = [
            {
                'notation': notation,
                'distance': ciede2000(bgr2lab(bgr), bgr2lab(center_bgr))
            }
            for notation, center_bgr in self.dynamic_palette.items()
        ]
        closest = min(distances, key=lambda x: x['distance'])
        print(f"🎯 Detected BGR: {tuple(int(c) for c in bgr)} → Notation: {closest['notation']} (distance={closest['distance']:.2f})")
        return closest['notation']

    def set_palette_by_centers(self, center_bgrs):
        """
        Sets the color→notation mapping using the center BGR values from the 6 face images.

        :param center_bgrs: Dict of {notation: center_bgr}
        """
        self.dynamic_palette = {}
        for notation, bgr in center_bgrs.items():
            self.dynamic_palette[notation] = bgr
