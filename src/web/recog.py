import numpy as np
from PIL import Image

from skimage import io
from skimage.color import rgba2rgb
from skimage.segmentation import slic
from skimage.segmentation import mark_boundaries
from skimage.util import img_as_float

from tensorflow import keras
import matplotlib.pyplot as plt

from keras.models import load_model
from keras.utils import img_to_array


# ML
model = load_model('models/keras_model.hdf5', compile=False)

leafTypes = ['bg', 'healthy', 'gls', 'nlb', 'nls']


def recognize(img):
    res = []

    img = Image.fromarray(img).resize((256, 256))
    segments = slic(img_as_float(img), n_segments=20, sigma=5)

    for (i, segVal) in enumerate(np.unique(segments)):
        temp_i = i
        mask = np.zeros(img.size[:2], dtype="uint8")
        mask[segments == segVal] = 255
        extracted_mask = np.stack(np.nonzero(mask), axis=-1)
        im = Image.fromarray(mask)
        cropped_segment = im.crop((min(extracted_mask[:, 1]), min(
            extracted_mask[:, 0]), max(extracted_mask[:, 1]), max(extracted_mask[:, 0])))
        cropped_img_segment = img.crop((min(extracted_mask[:, 1]), min(
            extracted_mask[:, 0]), max(extracted_mask[:, 1]), max(extracted_mask[:, 0])))
        temp = np.array(cropped_segment)/255
        output = np.array(cropped_img_segment)

        for i in range(3):
            final_result = np.multiply(
                temp, (np.array(cropped_img_segment)[:, :, i]))
            output[:, :, i] = final_result
        final_seg = Image.fromarray(output)

        seg = img_to_array(final_seg)
        seg = np.expand_dims(seg, axis=0)
        seg = seg.astype('float') / 255.0

        out = model.predict(seg)
        leafType = leafTypes[np.argmax(out)]
        # if confidence is 100 percent
        if (round(np.max(out), 2)): res.append({"segment": i, "prediction": leafType, "confidence": round(np.max(out), 2), "segment_data": mask})

    return res