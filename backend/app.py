from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
import kociemba
from collections import Counter
from qbr.image_solver import solve_cube_from_images

app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# === Count increment logic ===
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

# === Return cube count ===
@app.route('/cube-count', methods=['GET'])
def cube_count():
    path = os.path.join(os.path.dirname(__file__), 'cube_count.json')
    if not os.path.exists(path):
        return jsonify({"count": 0})
    with open(path) as f:
        count = json.load(f)['solved']
    return jsonify({"count": count})

# === Main Upload Endpoint ===
@app.route('/upload-images', methods=['POST'])
def upload_images():
    print("✅ Upload endpoint hit")

    face_keys = ['face1', 'face2', 'face3', 'face4', 'face5', 'face6']
    face_labels = ['U', 'R', 'F', 'D', 'L', 'B']
    image_paths = []

    # Step 1: Save uploaded images
    for key, face in zip(face_keys, face_labels):
        if key not in request.files:
            return jsonify({"error": f"Missing image: {key}"}), 400
        file = request.files[key]
        filename = f"{face}.jpg"
        path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(path)
        image_paths.append(path)

    try:
        # Step 2: Use QBR to generate cube string
        cube_string = solve_cube_from_images(image_paths)
        print("🧊 Cube String:", cube_string)

        # Step 3: Validate cube string
        if len(cube_string) != 54:
            return jsonify({
                "message": "❌ Invalid cube string length",
                "cube_string": cube_string
            }), 400

        color_counts = Counter(cube_string)
        if any(count != 9 for count in color_counts.values()):
            return jsonify({
                "message": "❌ Invalid color counts",
                "cube_string": cube_string,
                "counts": dict(color_counts)
            }), 400

        # Step 4: Solve
        solution = kociemba.solve(cube_string)
        increment_cube_count()

        return jsonify({
            "message": "✅ Cube solved successfully",
            "cube_state": cube_string,
            "solution": solution
        })

    except Exception as e:
        print("❌ Error:", str(e))
        return jsonify({
            "message": "❌ Error processing cube",
            "error": str(e)
        }), 500

if __name__ == "__main__":
    app.run(debug=True)
