from flask import Flask, jsonify, render_template, request, redirect, url_for
import os
import get_caption as gc
from PIL import Image

app = Flask(__name__)
max_size_mb = 1
max_quality = 85
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024
# def process_image(image_path):
#     captions = ["Caption 1", "Caption 2", "Caption 3", "Caption 4", "Caption 5"]
#     return captions


@app.route('/privacy_policy')
def privacy_policy():
    return render_template('privacypolicy.html')


@app.route('/', methods=['GET'])
def index():
    return render_template('result.html')

def compress_image(file_path):
    try:
        # Open the image file
        with Image.open(file_path) as img:
            # Compress the image with varying quality until it's below 1MB
            quality = max_quality
            while os.path.getsize(file_path) / (1024 * 1024.0) > max_size_mb and quality > 0:
                img.save(file_path, 'JPEG', quality=quality)
                quality -= 5  # Reduce quality by 5 in each iteration
    except Exception as e:
        print(f"Error during compression: {e}")

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)

    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        original_size = os.path.getsize(file_path) / (1024 * 1024.0)  

        if original_size >= max_size_mb:
            compress_image(file_path)

        captions = gc.get_caption_gemini(file_path)

        return jsonify({"captions": captions})

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, debug=False)
