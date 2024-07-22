from flask import Flask, jsonify, send_from_directory, render_template, request, send_file, jsonify
import os
from datetime import datetime
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("history.html")

# Path to the folders containing images
HISTORY_FOLDER = os.path.join(app.root_path, 'history')
TEST_FOLDER = os.path.join(app.root_path, 'test')
SEGMENTS_FOLDER = os.path.join(app.root_path, 'segments')

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
    
    for subdir in os.listdir(SEGMENTS_FOLDER):
        subdir_path = os.path.join(SEGMENTS_FOLDER, subdir)
        if os.path.isdir(subdir_path):
            for filename in os.listdir(subdir_path):
                if filename.endswith(('.jpg', '.jpeg', '.png')):
                    file_path = os.path.join(subdir_path, filename)
                    file_info = os.stat(file_path)
                    modification_time = datetime.fromtimestamp(file_info.st_mtime).strftime('%d/%m/%Y')
                    images.append({'filename': filename, 'date': modification_time, 'folder': 'segments', 'subfolder': subdir, 'path': f'/images/segments/{subdir}/{filename}'})
    
    print(images)
    return jsonify(images)

@app.route('/images/<folder>/<filename>', methods=['GET'])
@app.route('/images/<folder>/<subfolder>/<filename>', methods=['GET'])
def get_image(folder, filename, subfolder=None):
    if subfolder:
        folder_path = os.path.join(app.root_path, folder, subfolder)
    else:
        folder_path = os.path.join(app.root_path, folder)
    
    if os.path.exists(os.path.join(folder_path, filename)):
        return send_from_directory(folder_path, filename)
    else:
        return "File not found", 404
    
@app.route("/askGPT", methods=['POST'])
def chatGPT():
    def chatGPT(ques):
        url = "https://chatgpt-api8.p.rapidapi.com/"

        payload = [
            {
                "content": "Hello! I'm an AI assistant bot based on ChatGPT 3. How may I help you?",
                "role": "system"
            },
            {
                "content": f"{ques}",
                "role": "user"
            }
        ]
        headers = {
            "content-type": "application/json",
            "X-RapidAPI-Key": "030c80dc47mshbe06ccceee3100cp18b554jsnc6867b4f1b65",
            "X-RapidAPI-Host": "chatgpt-api8.p.rapidapi.com"
        }
        # huytrongnghia: 8dd3bfa3f3mshda3845149bb330ep1c4505jsna147eee499b5
        # khkt: d89a8977f9mshd28e97843a01cf2p158370jsn0cb69019b238
        # huynghia: 8eacc0c16dmshb79a0fe65bc3344p14e02ajsn29bf84e2e8b9
        # huytrong: 030c80dc47mshbe06ccceee3100cp18b554jsnc6867b4f1b65
        # nguyenquynh: 0c6c1ec218msh58fce662b00a268p1e2172jsn77027176568f

        response = requests.post(url, json=payload, headers=headers)
        data = response.json()

        return data["text"]

    try:
        data = request.json
        user_message = data['message']

        # Call your ChatGPT function here
        bot_message = chatGPT(user_message)

        return jsonify({'content': bot_message})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

# cấu trúc thư mục:
# app/
# ├── app.py 
# ├── static/                        
# │   ├── style.css                  
# │   └── script.js      
# ├── templates/                     
# │   └── history.html 
# ├── history
# ├── test
# └── segments 