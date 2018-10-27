from get_image import get_image, save_image, show_image
from classifiers import get_gold
import time

if __name__ == '__main__':
    time.sleep(5)
    a = time.time()
    initial_image = get_image()
    old_gold = get_gold(initial_image)
    new_image = get_image()
    new_gold = get_gold(initial_image)
    well_behaved = True
    while well_behaved and time.time() - a < 40*60:
        #roll back previous values
        old_gold = new_gold
        initial_image = new_image

        new_image = get_image()
        new_gold = get_gold(new_image)
        print new_gold
        well_behaved = ((new_gold == old_gold) or 
                        (new_gold == old_gold + 1))
    if not well_behaved:
        print "Error while counting gold"
        print "old: ", old_gold
        print "new: ", new_gold
        save_image(initial_image, 'gold0.png')
        save_image(new_image, 'gold1.png')
        show_image(initial_image)
        show_image(new_image)
    else:
        print "program well behaved"
        # show_image(new_image) # to exit client
