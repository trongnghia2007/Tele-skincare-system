from flask import Flask, jsonify, send_from_directory, render_template
import os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("map.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
   
# cấu trúc thư mục:
# app/
# ├── backend.py 
# ├── static/                        
# │   ├── style.css                  
# │   └── script.js      
# │   └── images/               
# └── templates/                     
#     └── handbook.html                 