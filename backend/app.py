from flask import Flask, jsonify
# removed photo/upload endpoints

app = Flask(__name__)

@app.route('/cube-count')
def cube_count():
    # existing logic to count solved cubes
    return jsonify({'count': get_cube_count()})

# deprecated upload_photo route removed

if __name__ == '__main__':
    app.run(debug=True)