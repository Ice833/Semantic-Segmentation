import os
from PIL import Image

img_dir = './img/'

img_list = os.listdir(img_dir)
for jpg in img_list:
    path = os.path.join(img_dir, jpg)
    img = Image.open(path)
    img_w, img_h = img.size
    cropped_img = img.crop((2, 0, img_w - 2, img_h))
    save_dir = './crop_img'
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
    cropped_img.save(os.path.join(save_dir,jpg))