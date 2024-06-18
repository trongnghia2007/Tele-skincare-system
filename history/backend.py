from flask import Flask, jsonify, send_from_directory, render_template, request
import os
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("history.html")

# Path to the folder containing medical images
IMAGE_FOLDER = 'history'

@app.route('/images', methods=['GET'])
def list_images():
    images = []
    for filename in os.listdir(IMAGE_FOLDER):
        if filename.endswith(('.jpg', '.jpeg', '.png')):
            file_path = os.path.join(IMAGE_FOLDER, filename)
            file_info = os.stat(file_path)
            modification_time = datetime.fromtimestamp(file_info.st_mtime).strftime('%d/%m/%Y')
            images.append({'filename': filename, 'date': modification_time, 'folder': IMAGE_FOLDER, 'path': f'/images/history/{filename}'})
    print(images)
    return jsonify(images)

@app.route('/images/<folder>/<filename>', methods=['GET'])
def get_image(folder, filename):
    folder_path = os.path.join(os.getcwd(), folder)  # Lấy đường dẫn đầy đủ đến thư mục
    if os.path.exists(os.path.join(folder_path, filename)):
        print(os.path.join(folder_path, filename))
        return send_from_directory(folder_path, filename)
    else:
        return "File not found", 404

@app.route('/find_image', methods=['POST'])
def find_image():
    data = request.get_json()
    filename = data.get('filename')
    file_path = os.path.join('test', filename)
    if os.path.exists(file_path):
        return jsonify({'found': True, 'path': f'/images/{file_path}'})
    else:
        return jsonify({'found': False})

if __name__ == '__main__':
    if not os.path.exists(IMAGE_FOLDER):
        print(f"Error: The directory '{IMAGE_FOLDER}' does not exist.")
    else:
        print(f"The directory '{IMAGE_FOLDER}' exists and contains: {os.listdir(IMAGE_FOLDER)}")
        app.run(debug=True)
