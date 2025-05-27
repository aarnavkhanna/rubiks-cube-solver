from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import kociemba
from collections import Counter
from auto_color_detection import get_cube_state_from_images
import json

app = Flask(__name__)
CORS(app)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# === Cube Count Helper ===
def increment_cube_count():
    path = os.path.join(os.path.dirname(__file__), 'cube_count.json')
    if not os.path.exists(path):
        with open(path, 'w') as f:
            json.dump({'solved': 0}, f)

    with open(path, 'r+') as f:
        data = json.load(f)
        data['solved'] += 1
        f.seek(0)
        json.dump(data, f)
        f.truncate()

@app.route('/cube-count', methods=['GET'])
def cube_count():
    path = os.path.join(os.path.dirname(__file__), 'cube_count.json')
    if not os.path.exists(path):
        return jsonify({ "count": 0 })
    with open(path) as f:
        count = json.load(f)['solved']
    return jsonify({ "count": count })

# === Main Upload Route ===
@app.route('/upload-images', methods=['POST'])
def upload_images():
    print("✅ Image upload endpoint hit")

    face_paths = []
    for i in range(1, 7):
        key = f'face{i}'
        if key not in request.files:
            return jsonify({"error": f"Missing image: {key}"}), 400
        file = request.files[key]
        save_path = os.path.join(UPLOAD_FOLDER, f"{key}.jpg")
        file.save(save_path)
        face_paths.append(save_path)

    try:
        cube_state = get_cube_state_from_images(face_paths)
        print("🧊 Cube State:", cube_state)

        color_counts = Counter(cube_state)
        print("🧩 Color Counts:", color_counts)

        if len(cube_state) != 54 or any(count != 9 for count in color_counts.values()):
            return jsonify({
                "message": "❌ Invalid cube string",
                "cube_state": cube_state,
                "color_counts": dict(color_counts)
            }), 400

        solution = kociemba.solve(cube_state)
        print("✅ Solution:", solution)

        # ✅ Count this as a solved cube
        increment_cube_count()

        return jsonify({
            "message": "Cube solved successfully",
            "cube_state": cube_state,
            "solution": solution
        })

    except Exception as e:
        print("❌ Error:", str(e))
        return jsonify({
            "message": "Error processing cube",
            "error": str(e)
        }), 500

if __name__ == "__main__":
    app.run(debug=True)
