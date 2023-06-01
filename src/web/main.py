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

        # get a list of predicted disease
        arr = []
        for i in res: 
            if i["prediction"] not in arr:
                arr.append(i["prediction"])

        # create an object for storing mask
        mask_init = np.zeros([256,256],dtype=np.uint8)
        mask_init.fill(0)
        mask_obj = {key: mask_init for key in arr}

        print(mask_obj)

        # loop over result -> stacking masks
        for i in range(len(res)):
            mask = res[i]["segment_data"]
            mask_obj[res[i]["prediction"]] = mask_obj[res[i]["prediction"]] + mask

        # applying mask
        for (k, v) in mask_obj.items():
            # load the image onto an numpy array
            img_arr = np.array(image)
            # seperate RGB layers from the image
            layer1, layer2, layer3 = img_arr[:, :, 0], img_arr[:, :, 1], img_arr[:, :, 2]
            # apply mask to each layer in the image
            layer1, layer2, layer3 = (layer1 * v), (layer2 * v), (layer3 * v)
            # stack RGB layers to make the masked color image
            layer0 = np.invert(np.dstack([layer1, layer2, layer3]))
            # convert the image background to black
            layer0[v == 0] = 0
            # saving the image
            filename = f"predict_{str(k)}.jpg"
            content.append({"prediction": str(k), "segment_data": filename})
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