#!/usr/bin/python
#
# Generates relevant bitmaps for convolution when searching for fonts.
# Maybe will be used to store and load templates for creeps, heroes, etc.

import numpy as np
from skimage.transform import resize

from get_image import load_image, show_image, compare_image_to_result

# link to images which contain the font's characters
image_file_regular = 'regular_inverted.png'
image_file_bold = 'bold_inverted.png'

# returning tuple is more generalizable
def get_crop_dimensions(image):
    '''returns (x0, x1, y0, y1), where
    image[x0:x1,y0:y1] removes only zero values from image
    '''
    dims = image.shape
    x0, x1, y0, y1 = (0,-1,0,-1)
    for x in range(dims[0]):
        if np.count_nonzero(image[x]) > 0:
            x0 = x
            break
    for x in range(dims[0]-1,-1,-1):
        if np.count_nonzero(image[x]) > 0:
            x1 = x
            break
    for y in range(dims[1]):
        if np.count_nonzero(image[:,y]) > 0:
            y0 = y
            break
    for y in range(dims[1]-1,-1,-1):
        if np.count_nonzero(image[:,y]) > 0:
            y1 = y
            break
    return x0,x1,y0,y1

def get_separators(image):
    '''returns list of separators, or column values,
    which would split image into separate character sub-images.
    aka a length 2 list for 1 char, length 3 for 2 char, etc.
    '''
    dims = image.shape
    x0,x1,y0,y1 = get_crop_dimensions(image)
    zeroes = []
    for y in range(y0,y1+1):
        if np.count_nonzero(image[:,y]) == 0:
            zeroes.append(y)
    separators = []
    separators.append(y0)
    for i in range(len(zeroes)):
        if len(separators) == 0 or zeroes[i-1] != zeroes[i]-1:
            separators.append(zeroes[i])
    separators.append(y1)
    # finally, fix case where two characters have been joined
    # doesn't work with 3+ characters, haven't observed this to occur
    i = 0
    while i < len(separators)-2: # unpythonic fix for insert into incrementing list
        if separators[i+1]-separators[i] > (x1-x0)*1.25: #width > height*1.25
            separators.insert(i+1, separators[i]+(separators[i+1]-separators[i])/2)
        i += 1
    return separators

from collections import defaultdict
def cache_results(func):
    cache = defaultdict(lambda: None)
    def wrapper(*args):
        if cache[args] == None:
            print "NEW ARG:", args
            cache[args] = func(*args)
        return cache[args]
    return wrapper

@cache_results
def hypatia_sans_regular(height):
    '''returns dict of images of height <height>
    for each character of the hypatia sans font
    currently supported: 0123456789+
    '''
    hypatia_templates = {}
    all_chars_uncropped = load_image(image_file_regular)
    x0,x1,y0,y1 = get_crop_dimensions(all_chars_uncropped)
    get_separators(all_chars_uncropped)
    all_chars = all_chars_uncropped[x0:x1,:,0]
    char_height = 1+x1-x0
    # show_image(all_chars)
    # These hard-coded values are really dangerous, editor beware
    hypatia_templates['1'] = resize(all_chars[:,0:120], (height, height*120/char_height))
    hypatia_templates['2'] = resize(all_chars[:,140:280], (height, height*140/char_height))
    hypatia_templates['3'] = resize(all_chars[:,290:430], (height, height*140/char_height))
    hypatia_templates['+'] = resize(all_chars[:,440:580], (height, height*140/char_height))
    hypatia_templates['4'] = resize(all_chars[:,580:730], (height, height*150/char_height))
    hypatia_templates['5'] = resize(all_chars[:,730:870], (height, height*140/char_height))
    hypatia_templates['6'] = resize(all_chars[:,870:1020], (height, height*150/char_height))
    hypatia_templates['7'] = resize(all_chars[:,1030:1160], (height, height*130/char_height))
    hypatia_templates['8'] = resize(all_chars[:,1170:1320], (height, height*150/char_height))
    hypatia_templates['9'] = resize(all_chars[:,1320:1470], (height, height*150/char_height))
    hypatia_templates['0'] = resize(all_chars[:,1470:1610], (height, height*140/char_height))
    
    # sk = ['1', '2', '3', '+', '4', '5', '6', '7', '8', '9', '0']
    # for key in sk:
    #     show_image(hypatia_templates[key])

    for key in hypatia_templates.keys():
        # show_image(hypatia_templates[key])
        # print hypatia_templates[key].shape
        hypatia_templates[key] = np.rot90(hypatia_templates[key], 2)
        # hypatia_templates[key] = hypatia_templates[key] - 0.5 # potential fix for '4' vs '+' issue
        # hypatia_templates[key][hypatia_templates[key] == 0] = -1 # potential fix for '4' vs '+' issue

    return hypatia_templates

@cache_results
def hypatia_sans_bold(height):
    '''returns dict of images of height <height>
    for each character of the hypatia sans font
    currently supported: 0123456789+
    '''
    hypatia_templates = {}
    all_chars_uncropped = load_image(image_file_bold)
    x0,x1,y0,y1 = get_crop_dimensions(all_chars_uncropped)
    get_separators(all_chars_uncropped)
    all_chars = all_chars_uncropped[x0:x1,:,0]
    char_height = 1+x1-x0
    # show_image(all_chars)
    # These hard-coded values are really dangerous, editor beware
    hypatia_templates['1'] = resize(all_chars[:,0:120], (height, height*120/char_height))
    hypatia_templates['2'] = resize(all_chars[:,140:310], (height, height*170/char_height))
    hypatia_templates['3'] = resize(all_chars[:,310:450], (height, height*140/char_height))
    hypatia_templates['+'] = resize(all_chars[:,450:620], (height, height*170/char_height))
    hypatia_templates['4'] = resize(all_chars[:,610:770], (height, height*160/char_height))
    hypatia_templates['5'] = resize(all_chars[:,770:920], (height, height*150/char_height))
    hypatia_templates['6'] = resize(all_chars[:,920:1080], (height, height*160/char_height))
    hypatia_templates['7'] = resize(all_chars[:,1080:1240], (height, height*160/char_height))
    hypatia_templates['8'] = resize(all_chars[:,1240:1400], (height, height*160/char_height))
    hypatia_templates['9'] = resize(all_chars[:,1400:1550], (height, height*150/char_height))
    hypatia_templates['0'] = resize(all_chars[:,1550:1710], (height, height*160/char_height))
    
    # sk = ['1', '2', '3', '+', '4', '5', '6', '7', '8', '9', '0']
    # for key in sk: #hypatia_templates.keys():
    #     show_image(hypatia_templates[key])

    for key in hypatia_templates.keys():
        # print hypatia_templates[key].shape
        hypatia_templates[key] = np.rot90(hypatia_templates[key], 2)
        # hypatia_templates[key] = hypatia_templates[key] - 0.5 # potential fix for '4' vs '+' issue
        # hypatia_templates[key][hypatia_templates[key] == 0] = -1 # potential fix for '4' vs '+' issue

    return hypatia_templates

# preload certain values
hypatia_sans_regular(17)

if __name__ == '__main__':
    # show_image(hypatia_sans_regular(12)['4']) # example syntax
    # hypatia_sans_regular(16) # death timers
    hypatia_sans_regular(17) # attack dmg
    hypatia_sans_bold(12)
    # hypatia_sans_regular(26) # cooldowns
