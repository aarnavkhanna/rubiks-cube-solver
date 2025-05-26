def classify_color(h, s, v):
    if s < 50 and v > 200:
        return 'W'  # White
    if h < 10 or h > 160:
        return 'R'  # Red
    if 10 <= h < 25:
        return 'O'  # Orange
    if 25 <= h < 35:
        return 'Y'  # Yellow
    if 35 <= h < 85:
        return 'G'  # Green
    if 85 <= h < 140:
        return 'B'  # Blue
    return '?'     # Unknown
