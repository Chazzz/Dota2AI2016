import numpy as np
import time
from scipy.signal import convolve2d
# local imports
from get_image import load_image, show_image
from creep_templates import rad_template, dir_template
from hero_templates import hero_template, ally_template, enemy_template
from font_templates import (
    get_crop_dimensions,
    get_separators,
    hypatia_sans_regular,
    hypatia_sans_bold,
    )
from creep_utils import Creep

def match_exact_template(img, template_img):
    '''x is vertical dimension, y is horizontal dimension
    The chances of a random pixel exactly matching is about 1 in 8 in 1080p.
    This gets exponentially smaller as the size of the template increases.'''
    # print .shape
    xs, ys = ([], [])
    # xs_raw, ys_raw = np.where((img == (42,110,59)).all(axis=2)) 6x slower
    xs_raw, ys_raw = np.where(
        ((img[:,:,0] == template_img[0,0,0])&
         (img[:,:,1] == template_img[0,0,1])&
         (img[:,:,2] == template_img[0,0,2])))
    t_height, t_width, t_depth = template_img.shape
    for x,y in zip(xs_raw,ys_raw):
        # if (img[x:x+t_height,y:y+t_width,0:3]==template_img).all():
        if np.array_equal(img[x:x+t_height,y:y+t_width,0:3],template_img):
            xs.append(x)
            ys.append(y)
    return xs, ys

def get_radiant_creeps(img, coords=(0, -1, 0, -1)):
    creeps = []
    xs, ys = match_exact_template(
        img[coords[2]:coords[3],coords[0]:coords[1]], rad_template)
    for x, y in zip(xs, ys):
        x = x + coords[2]
        y = y + coords[0]
        health = np.sum(img[x,y:y+78,0] > 35)/78.0
        creeps.append(Creep(y, x, health, time.time()))
    return creeps

def get_dire_creeps(img, coords=(0, -1, 0, -1)):
    creeps = []
    xs, ys = match_exact_template(
        img[coords[2]:coords[3],coords[0]:coords[1]], dir_template)
    for x, y in zip(xs, ys):
        x = x + coords[2]
        y = y + coords[0]
        health = np.sum(img[x,y:y+78,0] > 35)/78.0
        creeps.append(Creep(y, x, health, time.time()))
    return creeps

def get_hero(img, coords=(0, -1, 0, -1)):
    xs, ys = match_exact_template(
        img[coords[2]:coords[3],coords[0]:coords[1]], hero_template)
    return xs, ys

def get_ally(img, coords=(0, -1, 0, -1)):
    xs, ys = match_exact_template(
        img[coords[2]:coords[3],coords[0]:coords[1]], ally_template)
    return xs, ys

def get_enemy(img, coords=(0, -1, 0, -1)):
    xs, ys = match_exact_template(
        img[coords[2]:coords[3],coords[0]:coords[1]], enemy_template)
    return xs, ys

def num_mask_to_str(mask, font=hypatia_sans_regular):
    "perform optical character recognition on mask and return the string"
    answer = ""
    x0,x1,y0,y1 = get_crop_dimensions(mask)
    if (x0,x1,y0,y1) == (0,-1,0,-1): # BLACK IMAGE
        return ''
    separators = get_separators(mask)
    char_templates = font(mask.shape[0])
    mask = mask-0.5 # Go from [0-1] to [-0.5-0.5]
    results = []
    sorted_keys = sorted(char_templates.keys())
    for key in sorted_keys: # +,0,1...
        result = convolve2d(mask, char_templates[key],mode='valid')
        centering_offset = np.zeros((1,char_templates[key].shape[1]/2))
        results.append(np.concatenate((centering_offset, result), axis=1)[0])
    for i in range(len(separators)-1):
        peaks = [max(result[separators[i]:separators[i+1]]) for result in results]
        answer += sorted_keys[peaks.index(max(peaks))]
    return answer

def get_damage_mask(image):
    '''get mask which shows the attack damage of selected unit'''
    mask = image[1292*3/4:1309*3/4,915*3/4:1030*3/4,1] > 100
    return mask

def get_attack_dmg(image):
    res = num_mask_to_str(get_damage_mask(image), font=hypatia_sans_bold)
    if res == '':
        return 0
    else:
        return eval(res)

def get_gold_mask(image):
    '''get mask which shows the attack damage of selected unit'''
    mask = image[892:904,1750:1805,1] > 100
    return mask

def get_gold(image):
    res = num_mask_to_str(get_gold_mask(image))
    if res == '':
        return 0
    else:
        return eval(res)

if __name__ == '__main__':
    print "radiant creeps (4)"
    test_img = load_image("init.png")
    a = time.time()
    res = get_radiant_creeps(test_img)
    print time.time() - a
    print res
    print 'dire creeps (none)'
    a = time.time()
    res = get_dire_creeps(test_img)
    print time.time() - a
    print res
    print 'hero'
    test_img = load_image("dire_9520hp_2.png")
    a = time.time()
    res = get_hero(test_img)
    print time.time() - a
    print res
    print "ally"
    test_img = load_image("ally_4.png")
    a = time.time()
    res = get_ally(test_img)
    print time.time() - a
    print res
    print "enemy (2)"
    test_img = load_image("enemy_low_high.png")
    a = time.time()
    res = get_enemy(test_img)
    print time.time() - a
    print res
    test_img = load_image("enemy_low_high.png")
    print 51, get_attack_dmg(test_img)
    test_img = load_image("ally_4.png")
    print 55, get_attack_dmg(test_img)
    test_img = load_image("init.png")
    # print 39+9, get_attack_dmg(test_img)
    # show_image(test_img)
    print 107, get_gold(test_img)
    # show_image(get_damage_mask(test_img))
    # show_image(get_gold_mask(test_img))