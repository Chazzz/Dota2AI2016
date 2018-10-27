import numpy as np
from scipy.misc import imread
from matplotlib import pyplot as plt
import time

def bgrtorgb(image):
    '''swaps blue and red channels, important for loading/saving images'''
    redrow = image[:,:,2]
    greenrow = image[:,:,1]
    bluerow = image[:,:,0]
    return np.dstack([redrow,greenrow,bluerow])

def load_image(imagename):
    return bgrtorgb(imread(imagename))


def show_image(image):
    '''usage:
        show_image(load_image('abyssal blade.png'))
        show_image(get_image())

    also usable for 
    '''
    if image.ndim == 3:
        plt.imshow(image, interpolation='nearest')
    else:
        plt.imshow(image, interpolation='nearest', cmap='gray')
    plt.show()

img = imread("creeps1080p.png")
print img.shape
# print img[544:548,1299:1303,:]
# print img[1299:1302,544:546,:]

# show_image(img)

cropimg = img[250:450, 600:900,:]
cropimg_2 = img[300:600, 800:1400,:]
# show_image(cropimg_2)
rad_template = img[360:366,649:650,:]
dir_template = img[346:352,905:906,:]
print dir_template.shape
# show_image(dir_template)


def match_exact_template(img, template_img):
    '''x is vertical dimension, y is horizontal dimension
    The chances of a random pixel exactly matching is about 1 in 8 in 1080p.
    This gets exponentially smaller as the size of the template increases.'''
    xs, ys = ([], [])
    xs_raw, ys_raw = np.where(
        np.logical_and(np.logical_and(img[:,:,0] == template_img[0,0,0],
                                      img[:,:,1] == template_img[0,0,1]),
                                      img[:,:,2] == template_img[0,0,2]))
    t_height, t_width, t_depth = template_img.shape
    for x,y in zip(xs_raw,ys_raw):
        if (img[x:x+t_height,y:y+t_width,:]==template_img).all():
            xs.append(x)
            ys.append(y)
    return xs, ys

def get_radiant_creeps(img):
    return match_exact_template(img, rad_template)

def get_dire_creeps(img):
    return match_exact_template(img, dir_template)


a = time.time()
res = get_radiant_creeps(img)
print time.time() - a
print res
a = time.time()
res = get_dire_creeps(img)
print time.time() - a
print res
# show_image(img)
# show_image(np.logical_and(np.logical_and(img[:,:,0] == img[544,1299,0], img[:,:,1] == img[544,1299,1]), img[:,:,2] == img[544,1299,2]))