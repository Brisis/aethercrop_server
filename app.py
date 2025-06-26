import os
from flask import Flask, request, send_file
from rembg import remove
from werkzeug.utils import secure_filename
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/remove-bg', methods=['POST'])
def remove_bg():
    if 'image' not in request.files:
        return {'error': 'No image uploaded'}, 400

    file = request.files['image']
    filename = secure_filename(file.filename)
    input_path = os.path.join(UPLOAD_FOLDER, filename)
    output_path = os.path.join(UPLOAD_FOLDER, f"removed_{filename}")

    file.save(input_path)
    with open(input_path, 'rb') as inp, open(output_path, 'wb') as outp:
        output_data = remove(inp.read())
        outp.write(output_data)

    return send_file(output_path, mimetype='image/png')


if __name__ == "__main__":
    # Use Render's PORT variable or fallback to 9000 locally
    port = int(os.getenv("PORT", 9000))
    app.run(host="0.0.0.0", port=port)