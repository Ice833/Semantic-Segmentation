import os
import copy
from PIL import Image, ImageDraw, ImageFont

img_dir = "./img_out/"
label_file = "./coalPercentage.txt"
time_file = "./timeSpend.txt"
imgs_label = "./imgs_label2/"

if not os.path.exists(imgs_label):
    os.mkdir(imgs_label)


def text_label(_img, _str):
    new_img = copy.deepcopy(_img)
    draw = ImageDraw.Draw(new_img)

    font = ImageFont.truetype("arial.ttf", 15)
    draw.text((20, 20), _str, fill='#ffffff', font=font)
    return new_img


with open(label_file, 'r') as lf, open(time_file, 'r') as tf:
    line2 = tf.read()
    for line1 in lf:
        m = line1.find(' ')
        end = line1.find('\n')
        img_name = line1[:m]
        img = Image.open(img_dir + img_name)
        p = line1[m:end]

        m_t = line2.find(img_name) + 7
        end_t = m_t + 7
        t = line2[m_t:end_t]
        str_lbl = p + '   ' + 'time_cost:' + t
        img_n = text_label(img, str_lbl)
        img_n.save(imgs_label + img_name)

end_log = 'Processing finish!'
print(end_log)
