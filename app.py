import os
from flask import Flask, request, send_file
from rembg import remove
from werkzeug.utils import secure_filename
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for Nuxt frontend

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/remove-bg', methods=['POST'])
def remove_bg():
    if 'image' not in request.files:
        return {'error': 'No image uploaded'}, 400
    
    file = request.files['image']
    filename = secure_filename(file.filename)
    input_path = os.path.join(UPLOAD_FOLDER, filename)
    output_path = os.path.join(UPLOAD_FOLDER, f"removed_{filename}")

    file.save(input_path)
    
    # Remove background
    with open(input_path, 'rb') as inp, open(output_path, 'wb') as outp:
        input_data = inp.read()
        output_data = remove(input_data)
        outp.write(output_data)
    
    # Return processed image
    return send_file(output_path, mimetype='image/png')