from nets.segnet import mobilenet_segnet
from PIL import Image
import numpy as np
import time as t
import copy
import os



# class_colors = [[0,0,0],[0,255,0]]
# NCLASSES = 2
# HEIGHT = 416
# WIDTH = 416

class_colors = [[0,0,0],[255,0,0],[0,255,0]]
NCLASSES = 3
HEIGHT = 480
WIDTH = 848


model = mobilenet_segnet(n_classes=NCLASSES,input_height=HEIGHT, input_width=WIDTH)
model_dir ="logs/last1.h5"
model.load_weights(model_dir)

img_dir ="./img/"           #option: "./dataset2/jpg/"
imgs = os.listdir(img_dir)

imgs_label = "./imgs_label/"

if not os.path.exists(imgs_label):
    os.mkdir(imgs_label)

with open('timeSpend.txt', 'w') as f:
    for jpg in imgs:

        img = Image.open(img_dir+jpg)
        # img = Image.ImageEnhance.Contrast(img)
        old_img = copy.deepcopy(img)
        original_h = np.array(img).shape[0]
        original_w = np.array(img).shape[1]

        # Surpressing the original image to 1/4 of it own
        img = img.resize((WIDTH/2,HEIGHT/2))
        img = np.array(img)
        img = img/255
        img = img.reshape(-1,HEIGHT,WIDTH,3)

        # Adding timing
        ts = t.perf_counter()
        pr = model.predict(img)[0]
        tn = t.perf_counter()

        delta_t = str('{:.3f}'.format((tn - ts),))
        pr = pr.reshape((int(HEIGHT/2), int(WIDTH/2),NCLASSES)).argmax(axis=-1)

        seg_img = np.zeros((int(HEIGHT/2), int(WIDTH/2),3))
        colors = class_colors

        for c in range(NCLASSES):
            seg_img[:,:,0] += ((pr[:,: ] == c)*(colors[c][0])).astype('uint8')
            seg_img[:,:,1] += ((pr[:,: ] == c)*(colors[c][1])).astype('uint8')
            seg_img[:,:,2] += ((pr[:,: ] == c)*(colors[c][2])).astype('uint8')

        seg_img = Image.fromarray(np.uint8(seg_img)).resize((original_w,original_h))
        image = Image.blend(old_img,seg_img,0.3)
        image.save("./img_out/"+jpg)
        seg_img.save(os.path.join(imgs_label, jpg))
        f.write(jpg + ':' + delta_t + 's' + '\n')

end_log = 'Segmentation finished.'
print(end_log)