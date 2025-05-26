from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import kociemba

from video_processing import extract_6_faces
from auto_color_detection import get_cube_state_from_faces

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB limit
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route('/upload', methods=['POST'])
def upload_video():
    print("✅ Upload endpoint hit!")

    if 'video' not in request.files:
        return jsonify({"error": "No video file provided"}), 400

    file = request.files['video']
    filename = file.filename
    save_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(save_path)
    print(f"✅ Saved video as {save_path}")

    try:
        extract_6_faces(save_path)
        cube_state = get_cube_state_from_faces()
        print("✅ Cube state:", cube_state)

        solution = kociemba.solve(cube_state)
        print("✅ Solution:", solution)

        return jsonify({
            "message": "Cube processed successfully",
            "cube_state": cube_state,
            "solution": solution
        })

    except Exception as e:
        print("❌ Error:", str(e))
        return jsonify({
            "message": "Error while processing cube",
            "error": str(e)
        }), 500


# ✅ THIS IS CRITICAL
if __name__ == "__main__":
    app.run(debug=True)
