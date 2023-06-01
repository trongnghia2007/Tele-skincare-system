from skimage import io
from PIL import Image
import numpy as np
from temp2 import recognize

pic = io.imread("samplev3.jpg")
res = recognize(pic)
pic = Image.fromarray(pic).resize((256, 256))

print(res)

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

for (k, v) in mask_obj.items():
    print(f"Displaying: Mask for {str(k)}")

    Image.fromarray(v).show()

    img_arr = np.array(pic)
    layer1, layer2, layer3 = img_arr[:, :, 0], img_arr[:, :, 1], img_arr[:, :, 2]
    layer1, layer2, layer3 = (layer1 * v), (layer2 * v), (layer3 * v)

    layer0 = np.invert(np.dstack([layer1, layer2, layer3]))

    layer0[v == 0] = 0

    Image.fromarray(layer0).show()