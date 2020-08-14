import os
import PIL.Image as Image
import numpy as np
import copy
import matplotlib.pyplot as plt

class_colors = [[0, 0, 0], [255, 0, 0], [0, 255, 0]]
NCLASSES = 3
HEIGHT = 480
WIDTH = 848


def coal_percent(_img):

    r, g, _ = _img.split()
    rr = np.array(r.histogram())
    gg = np.array(g.histogram())
    end = len(rr) - 1

    tol = 5
    coal = np.sum(rr[end - tol: end])
    gangue = np.sum(gg[end - tol: end])
    percent_coal = coal / (coal + gangue)
    try:
        return percent_coal
    except ZeroDivisionError:
        print('No mine detection!')
        return 0


if __name__ == '__main__':

    img_dir = "./imgs_label/"
    imgs = os.listdir(img_dir)

    with open('coalPercentage.txt', 'w') as f:
        for jpg in imgs:
            img = Image.open(img_dir + jpg)
            percent = str('{:.2%}'.format(coal_percent(img)))
            f.write(jpg + ' coal:' + percent + '\n')

end_log = 'Processing finish!'
print(end_log)