from get_image import get_image, save_image, show_image
from classifiers import get_gold, get_attack_dmg, get_enemy
from user_input import buy_item
import time
import code

if __name__ == '__main__':
    time.sleep(0)
    s = time.time()
    bought = False
    counter = 0
    while not bought and time.time()-s < 3:
        image = get_image()
        gold = get_enemy(image)
        gold = get_enemy(image)
        gold = get_enemy(image)
        gold = get_enemy(image)
        # print "gold:", gold
        dmg = get_attack_dmg(image)
        counter += 1
        # print "damage:", dmg
        # if gold > 820:
        #     buy_item('phase boots')
        #     bought = True
    print counter/3.0
    print 1/(counter/3.0)



        # try:
        # except Exception as e:
        #     show_image(image)
        #     save_image(image, 'error.png')
        #     code.interact(local=dict(globals(), **locals()))