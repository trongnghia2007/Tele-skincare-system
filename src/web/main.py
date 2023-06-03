from flask import Flask, render_template, request, send_file, jsonify
from temp2 import recognize
import skimage 
from PIL import Image
import numpy as np
import io
import json

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/perform-leaf-recognition", methods=['GET', 'POST'])
def handle_recog():
    if request.method == "POST":
        image = (request.files['image'])
        image = skimage.io.imread(image)
        # try:
        res = recognize(image)
        image = Image.fromarray(image).resize((256, 256))
        content = []

        # applying mask
        for i in res:
            # load the image onto an numpy array
            img_arr = np.array(image)
            # seperate RGB layers from the image
            layer1, layer2, layer3 = img_arr[:, :, 0], img_arr[:, :, 1], img_arr[:, :, 2]
            # apply mask to each layer in the image
            mask = i["segment_data"]
            layer1, layer2, layer3 = (layer1 * mask), (layer2 * mask), (layer3 * mask)
            # stack RGB layers to make the masked color image
            layer0 = np.invert(np.dstack([layer1, layer2, layer3]))
            # convert the image background to black
            layer0[mask == 0] = 0
            # saving the image
            filename = f"seg-{i['segment']}_pred-{i['prediction']}_conf-{i['confidence']}.jpg"
            content.append({"prediction": i['prediction'], "segment_data": filename, "confidence": i['confidence']})
            Image.fromarray(layer0).save(f"test/{filename}.jpg")
        
        print(content)
        return jsonify(content)

        # except Exception as e: 
        #     return str(e)
        
@app.route('/images/<pid>.jpg')
def get_image(pid):
    pid = str(pid)
    img = skimage.io.imread(f"test/{pid}.jpg")
    img = Image.fromarray(img)
    file_object = io.BytesIO()    
    img.save(file_object, 'JPEG')
    file_object.seek(0)
    return send_file(file_object, mimetype='image/JPEG')

if __name__ == "__main__":
    app.run()