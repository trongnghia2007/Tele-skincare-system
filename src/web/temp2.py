from keras.models import load_model  # TensorFlow is required for Keras to work
from PIL import Image, ImageOps  # Install pillow instead of PIL
import numpy as np

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

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# ML
model = load_model('models/keras_model_recent.h5')

# Load the labels
class_names = ['sc', 'cp', 'der', 'healthy']

def predict_with_model(img, seg):

    # Create the array of the right shape to feed into the keras model
    # The 'length' or number of images you can put into the array is
    # determined by the first position in the shape tuple, in this case 1
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    # Replace this with the path to your image
    image = img.convert("RGB")

    # resizing the image to be at least 224x224 and then cropping from the center
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

    # turn the image into a numpy array
    image_array = np.asarray(image)

    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

    # Load the image into the array
    data[0] = normalized_image_array

    # Predicts the model
    prediction = model.predict(data)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]

    # Print prediction and confidence score
    print(f"seg: {seg} - Class: {class_name} - Confidence Score: {round(confidence_score, 2) * 100}")
    # print("Class:", class_name, end="")
    # print("Confidence Score:", confidence_score)

    return {"class_name": class_name, "confidence": confidence_score}

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

        # final_seg.show()
        
        # Make the prediction
        out = predict_with_model(final_seg, temp_i)

        # Process the prediction result
        # # setting a threshold 
        if (out["confidence"] > 0.9): 
            res.append({"segment": temp_i, "prediction": out['class_name'], "confidence": str(out['confidence']), "segment_data": mask})
            Image.fromarray(mask).save(f"segments/seg-{temp_i}_pred-{out['class_name']}_conf-{round(out['confidence'], 3)}.jpg")
            
        print(f"seg-{temp_i}_pred-{out['class_name']} \nConfidence: {round(out['confidence'], 3)}")

    return res

