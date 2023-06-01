import numpy as np
from PIL import Image
from base64 import b64decode, encodebytes
from rembg import remove

from skimage import io
import os
from skimage.color import rgba2rgb
from skimage.segmentation import slic
from skimage.util import img_as_float

from tensorflow import keras

from keras.models import load_model
from keras.utils import img_to_array
from keras.applications.imagenet_utils import preprocess_input


# ML
model = load_model('models/keras_model_recent.h5')

skinTypes = ['cp', 'sc', 'der', 'healthy']


def recognize(img):
    pathSave = 'segments/'

    skin_image = Image.fromarray(img).resize((256, 256))
    segments = slic(img_as_float(skin_image), n_segments=20, sigma=5)

    res = []

    # SLIC
    segNum = 0
    for (i, segVal) in enumerate(np.unique(segments)):
        temp_i = i
        mask = np.zeros(skin_image.size[:2], dtype="uint8")
        mask[segments == segVal] = 255
        extracted_mask = np.stack(np.nonzero(mask), axis=-1)
        im = Image.fromarray(mask)
        cropped_segment = im.crop((min(extracted_mask[:, 1]), min(
            extracted_mask[:, 0]), max(extracted_mask[:, 1]), max(extracted_mask[:, 0])))
        cropped_img_segment = skin_image.crop((min(extracted_mask[:, 1]), min(
            extracted_mask[:, 0]), max(extracted_mask[:, 1]), max(extracted_mask[:, 0])))
        temp = np.array(cropped_segment)/255
        output = np.array(cropped_img_segment)

        for i in range(3):
            final_result = np.multiply(
                temp, (np.array(cropped_img_segment)[:, :, i]))
            output[:, :, i] = final_result
        final_seg = Image.fromarray(output)

        resized_img = final_seg.resize((224, 224))
        resized_img_array = np.asarray(resized_img)
        preprocessed_img = preprocess_input(resized_img_array)

        # Make the prediction
        out = model.predict(np.expand_dims(preprocessed_img, axis=0))
        confidence = out[0][np.argmax(out)]


        # Process the prediction result
        # setting a threshold
        if (confidence >= 0.9): 
            res.append({"segment": temp_i, "prediction": skinTypes[np.argmax(out)], "confidence": round(np.max(out), 2), "segment_data": mask})
            Image.fromarray(mask).save(f"segments/seg-{temp_i}_pred-{skinTypes[np.argmax(out)]}_conf-{confidence}.jpg")
            
            
        print(f"seg-{temp_i}_pred-{skinTypes[np.argmax(out)]} \nConfidence: {confidence}")

    return res
