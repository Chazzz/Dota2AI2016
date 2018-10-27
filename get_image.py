#!/usr/bin/python
# get_image.py
# from get_image import get_image, load_image, save_image
#
# As an artifact of QPixmap conversion, red and blue channels are swapped
# relative to the rgbl .png format
# 
# cProfile indicates (for my 1440p setup)
# get_image takes about 0.05 seconds to run,
# a pretty significant bottleneck.
#
# See gtk_image and wx_image for slower versions of below code 
# Writing screen grabbing in C++, then exposing the pointer at bits
# would probably avoid most of the SIP overhead, maybe 2x speedup

import numpy as np
from scipy.misc import imsave, imread
from PyQt4.QtGui import QPixmap, QApplication, QImage
from matplotlib import pyplot as plt

app = QApplication([])

def bgrtorgb(image):
    '''swaps blue and red channels, important for loading/saving images'''
    redrow = image[:,:,2]
    greenrow = image[:,:,1]
    bluerow = image[:,:,0]
    return np.dstack([redrow,greenrow,bluerow])

def qimage_to_numpy(q_image):
    '''Converts a QImage object into a numpy array

    performance:
        .55 np.array()
        .45 i.bits()
    '''
    q_image = q_image.convertToFormat(4)

    width = q_image.width()
    height = q_image.height()

    ptr = q_image.bits()
    ptr.setsize(q_image.byteCount())
    arr = np.array(ptr).reshape(height, width, 4)  # Copies the data to a [b,g,r,l] array
    return arr

def get_image():
    '''Returns a 2-d array of the image on the screen.

    performance:
        .66 toImage()
        .33 convertQImageToMat()
    '''
    image = qimage_to_numpy(QPixmap.grabWindow(QApplication.desktop().winId()).toImage())
    return image

def load_image(imagename):
    return bgrtorgb(imread(imagename))

def save_image(image, imagename='temp.png'):
    imsave(imagename, bgrtorgb(image))

def show_image(image):
    '''usage:
        show_image(load_image('abyssal blade.png'))
        show_image(get_image())

    also usable for 
    '''
    if image.ndim == 3:
        plt.imshow(bgrtorgb(image), interpolation='nearest')
    else:
        plt.imshow(image, interpolation='nearest', cmap='gray')
    plt.show()

def compare_image_to_result(image, result):
    plt.subplot(1, 2, 1)
    plt.imshow(bgrtorgb(image), interpolation='nearest')
    plt.subplot(1, 2, 2)
    if np.max(result) == 1:
        plt.imshow(result, interpolation='nearest', cmap='gray')
    else:
        plt.imshow(result, interpolation='nearest')
        plt.colorbar()
    plt.show()
    return

if __name__ == '__main__':
    import time
    show_image(get_image())
    # -- python -m cProfile -s time -o out get_image.py --
    # for i in range(100):
    #     get_image()
    #     time.sleep(0.1) # intentionally de-optimize iterations