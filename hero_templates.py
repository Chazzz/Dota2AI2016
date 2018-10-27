# 1080p templates for dire and radiant creeps
from get_image import load_image, show_image, save_image, get_image
import time

fat_hero = load_image('9520hp.png')
ally_1 = load_image('ally_3.png')
enemy_hero = load_image('enemy_1.png')

hero_template = fat_hero[424:429,1032:1033]
# print hero_template

ally_template = ally_1[430:436,675:676]

enemy_template = enemy_hero[493:499,1042:1043]

# print enemy_template
# show_image(enemy_hero)

# time.sleep(5)
# image = get_image()
# save_image(image, 'enemy_low_high.png')
# show_image(image)