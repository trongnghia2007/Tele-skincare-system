from flask import Flask, jsonify, send_from_directory, render_template, request
import os
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("history.html")

# Path to the folder containing medical images
HISTORY_FOLDER = os.path.join(app.root_path, 'history')
TEST_FOLDER = os.path.join(app.root_path, 'test')

@app.route('/images', methods=['GET'])
def list_images():
    images = []
    for folder in [HISTORY_FOLDER, TEST_FOLDER]:
        folder_name = 'history' if folder == HISTORY_FOLDER else 'test'
        for filename in os.listdir(folder):
            if filename.endswith(('.jpg', '.jpeg', '.png')):
                file_path = os.path.join(folder, filename)
                file_info = os.stat(file_path)
                modification_time = datetime.fromtimestamp(file_info.st_mtime).strftime('%d/%m/%Y')
                images.append({'filename': filename, 'date': modification_time, 'folder': folder_name, 'path': f'/images/{folder_name}/{filename}'})
    print(images)
    return jsonify(images)

@app.route('/images/<folder>/<filename>', methods=['GET'])
def get_image(folder, filename):
    folder_path = os.path.join(app.root_path, folder)  # Lấy đường dẫn đầy đủ đến thư mục
    if os.path.exists(os.path.join(folder_path, filename)):
        return send_from_directory(folder_path, filename)
    else:
        return "File not found", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
