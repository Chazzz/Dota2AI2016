#!/usr/bin/python
#
# Actor

import code


from get_image import get_image, save_image, show_image
from user_input import (
    right_click,
    left_click,
    toggle,
    level_up,
    buy_item,
    say_in_chat,
    center_camera_on_hero,
    clear_cursor,
    )
from classifiers import (
    get_radiant_creeps,
    get_dire_creeps,
    get_gold,
    get_attack_dmg,
    )
from creep_utils import (
    get_threshold_creeps,
    get_lowest_creep,
    percent_health_melee,
    percent_health_ranged,
    hero,
    )
from creep_tracker import (
    index_creeps,
    )

import time
import random
import logging
import sys
import numpy as np #TODO: Remove on refactor

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

# top_right_area = (1200, -1, 60, 675)
# middle_area = (1000, 2200, 300, 900)
middle_area = (0, -1, 45, 900)

def initialize_state():
    # global variables do not change mid-execution
    # thus state provides an alternative namespace to store
    # persistent but dynamic values
    state = {
        'counter': 0,
        'fast_iterate': False,
        'last_command': '',
        'levels_in_e': 0,
        'start_time': time.time(),
        'hero_damage': 39,
        'gold': 0,
        'last_hits': 0,
        'rad_creeps_history': [],
        'dire_creeps_history': [],
        'lh_creeps_history': [],
        'rad_creeps': [],
        'dire_creeps': [],
    }
    return state

def startup(state):
    '''run once at beginning of program
    to force application into desired state for iteration
    '''
    buy_item('animal courier')
    time.sleep(0.1)
    toggle('z')
    time.sleep(1)
    buy_item('blades of attack') #('boots of speed')
    time.sleep(0.1)
    level_up('e')
    time.sleep(0.1)
    # toggle('a')
    # left_click(96, 1358)
    # right_click(796, 758)
    # time.sleep(2)
    right_click(70, 1015) # next to t3 mid
    time.sleep(12)
    center_camera_on_hero()
    time.sleep(0.1)
    say_in_chat(['-startgame'])
    time.sleep(1)
    state['start_time'] = time.time()

def log_action(state):
    # logging.debug("%i:%0.2f %s" % (
    #     ((time.time()-state['start_time'])/60),
    #     (time.time()-state['start_time'])%60,
    #     state['last_command'],
    #     )
    logging.debug("%i %s" % (
        state['counter'],
        state['last_command'],
        )
    )

def long_iterate(state):
    rand = int(random.random()*10)
    if rand%10 == 0:
        if state['levels_in_e'] < 3:
            level_up('e')
            time.sleep(0.3)
        level_up('w')
        if state['levels_in_e'] >= 3:
            time.sleep(0.3)
            level_up('u')
    if rand%10 == 1:
        time.sleep(0.1)
        buy_item('phase boots')
        time.sleep(0.05)
        toggle('f3')

def attack_ancient(state):
    if state['last_command'] != 'attack':
        state['last_command'] = 'attack'
        toggle('a')
        time.sleep(0.2) # Previously 0.1
        # Weird minimap interactions causing camera view to change???
        left_click(360*1080/1440,1100*1080/1440)
        log_action(state)

def move_to_ancient(state):
    if state['last_command'] != 'forward':
        right_click(360*1080/1440,1100*1080/1440)
        state['last_command'] = 'forward'
        log_action(state)

def attack_t2(state):
    if state['last_command'] != 'attack_t2':
        toggle('a')
        time.sleep(0.1)
        left_click(280*1080/1440, 1180*1080/1440)
        state['last_command'] = 'attack_t2'
        log_action(state)

def move_to_mid_t3(state):
    if True: #state['last_command'] != 'retreat':
        right_click(96*1080/1440,1348*1080/1440)
        state['last_command'] = 'retreat'
        log_action(state)

def stop(state):
    # time_last_hit is a form of stop, so no need to repeat command
    if state['last_command'] == 'time_last_hit':
        state['last_command'] = 'stop'
        return
    if state['last_command'] == 'retreat':
        move_to_ancient(state)
        time.sleep(0.1) # approx time to 180
    if state['last_command'] != 'stop':
        toggle('s')
        state['last_command'] = 'stop'
        center_camera_on_hero()
        log_action(state)

def hold_position(state):
    '''note: not actually used'''
    toggle('h')
    state['last_command'] = 'hold'
    center_camera_on_hero()
    log_action(state)

def attack_creep(state, creep):
    right_click(creep.x+30*1080/1440, creep.y+60*1080/1440)
    state['last_command'] = 'last_hit'
    time.sleep(0.8) # Don't move while attacking
    clear_cursor()
    log_action(state)

def inch_toward_creep(state, creep):
    if state['last_command'] != 'forward':
        # right_click(creep.x+30,creep.y+60)
        # state['last_command'] = 'forward'
        move_to_ancient(state)
        # clear_cursor()
        time.sleep(0.05)
        stop(state)
        log_action(state)

def last_hit(state, dire_creeps):
    # print "last_hitting"
    # print dire_creeps
    if dire_creeps:
        if len(dire_creeps) > 1:
            dmg_percent = percent_health_melee(state['hero_damage'])
            latency_percent = 0.0 #0.1
            soon_percent = percent_health_melee(state['hero_damage']) + 0.3
        else:
            dmg_percent = percent_health_ranged(state['hero_damage'])
            latency_percent = 0.0 #0.15
            soon_percent = percent_health_ranged(state['hero_damage']) + 0.4
        threshold_percent = dmg_percent+latency_percent
        # print threshold_percent
        lh_creeps = get_threshold_creeps(dire_creeps,
            (0.00,threshold_percent)
            )
        soon_lh_creeps = get_threshold_creeps(dire_creeps,
            (threshold_percent, dmg_percent+soon_percent)
            )
        # print lh_creeps
        if lh_creeps:
            attack_creep(state, lh_creeps[0])
            print "attack creep"
            lh_creeps[0].last_hit = state['counter']
            if len(dire_creeps) > 1:
                label = 'M'
            else:
                label = 'R'
            lh_creeps[0].label = label
            state['lh_creeps_history'].append(lh_creeps[0])
            return
        elif soon_lh_creeps:
            stop(state)
            state['last_command'] = 'time_last_hit'
            return
        else:
            attack_ancient(state)
            return
    else:
        attack_ancient(state)
        return

def get_num_buffer_creeps(rad_creeps):
    buffer_creeps = [creep for creep in rad_creeps if
        creep.x > 1200*1080/1440 and creep.y < 675*1080/1440]
    if len(buffer_creeps) > 1:
        return len(buffer_creeps)
    if len(buffer_creeps) == 1 and buffer_creeps[0].health > 0.9:
        return 1
    return 0

def get_num_backstab_creeps(dire_creeps):
    backstab_creeps = [creep for creep in dire_creeps if 
        creep.x < 1500*1080/1440 and creep.y > 400*1080/1440] # quadrant 3
    return len(backstab_creeps)

def in_range(dire_creeps):
    in_range_dist = 550*1080/1440
    lowest_creep = get_lowest_creep(dire_creeps)
    dist_to_creep = ((lowest_creep.x-hero.x)**2+(lowest_creep.y-hero.y)**2)**0.5
    return dist_to_creep < in_range_dist

def reposition(state, rad_creeps, dire_creeps, at_t2_5):
    '''transgress high ground iff creep buffer'''
    num_buffer_creeps = get_num_buffer_creeps(rad_creeps)
    if num_buffer_creeps >= 1:
        last_hit(state, dire_creeps)
        # if not state['quick_fire_funs']:
        #     long_iterate(state)
        return
    else:
        if at_t2_5:
            move_to_mid_t3(state) # regress to hiding behind creeps, not 100% functional
            return
        elif not dire_creeps:
            if state['counter']%10 == 0:
                state['last_command'] = 'stop' # help with respawn
            attack_ancient(state)
            # long_iterate(state) # comment out to help with t2.5 case
            return
        elif state['levels_in_e'] > 2 and not in_range(dire_creeps):
            attack_ancient(state)
            # long_iterate(state)
            return
        else:
            move_to_mid_t3(state)
            return

def update_rad_creeps(state, new_rad_creeps):
        old_creeps = state['rad_creeps']
        new_creeps = new_rad_creeps
        indexes = index_creeps(old_creeps, new_creeps)
        for i, creep in enumerate(new_creeps):
            if indexes[i] == -1:
                creep.birth_count = state['counter']
            else:
                # creep.label = old_creeps[indexes[i]].label
                creep.birth_count = old_creeps[indexes[i]].birth_count
                creep.x_history = (old_creeps[indexes[i]].x_history + 
                                  [old_creeps[indexes[i]].x])
                creep.y_history = (old_creeps[indexes[i]].y_history + 
                                  [old_creeps[indexes[i]].y])
                creep.health_history = (old_creeps[indexes[i]].health_history + 
                                       [old_creeps[indexes[i]].health])
                creep.time_history = (old_creeps[indexes[i]].time_history + 
                                     [old_creeps[indexes[i]].time])
        state['rad_creeps'] = new_creeps
        # add newly dead creeps to tracked_creeps_history
        for i in range(len(old_creeps)):
            if i not in indexes:
                state['rad_creeps_history'].append(old_creeps[i])

def update_dire_creeps(state, new_dire_creeps):
        old_creeps = state['dire_creeps']
        new_creeps = new_dire_creeps
        indexes = index_creeps(old_creeps, new_creeps)
        for i, creep in enumerate(new_creeps):
            if indexes[i] == -1:
                creep.birth_count = state['counter']
            else:
                # creep.label = old_creeps[indexes[i]].label
                creep.birth_count = old_creeps[indexes[i]].birth_count
                creep.x_history = (old_creeps[indexes[i]].x_history + 
                                  [old_creeps[indexes[i]].x])
                creep.y_history = (old_creeps[indexes[i]].y_history + 
                                  [old_creeps[indexes[i]].y])
                creep.health_history = (old_creeps[indexes[i]].health_history + 
                                       [old_creeps[indexes[i]].health])
                creep.time_history = (old_creeps[indexes[i]].time_history + 
                                     [old_creeps[indexes[i]].time])
        state['dire_creeps'] = new_creeps
        # add newly dead creeps to tracked_creeps_history
        for i in range(len(old_creeps)):
            if i not in indexes:
                state['dire_creeps_history'].append(old_creeps[i])

def midgame_iterate(state, code_interact=False):
    state['counter'] += 1
    if state['last_command'] != 'time_last_hit':
        if state['counter'] % 8 == 0 or state['last_command'] == 'retreat':
            center_camera_on_hero()
            # time.sleep(0.2) # time it takes after command to center camera
    image = get_image()
    # if state['save_counter'] == 200:
    #     save_image(image, '100.png')
    # if state['counter'] % 20 = 0:
    # Below "A or B" means "A unless A == 0 then B instead"
    state['hero_damage'] = get_attack_dmg(image) or state['hero_damage']
    state['levels_in_e'] = 1 #get_levels_in_e(image)
    state['minimap_position'] = 'todo' #get_minimap_position(image)
    at_t2_5 = False #is_at_t2_5(image)
    update_dire_creeps(state, get_dire_creeps(image, middle_area))
    update_rad_creeps(state, get_radiant_creeps(image, middle_area))
    # if state['hero_damage'] > 100:
    #     show_image(image)
    #     save_image(image, 'error.png')
    #     code.interact(local=dict(globals(), **locals()))
    reposition(state, state['rad_creeps'], state['dire_creeps'], at_t2_5)
    gold = get_gold(image)
    if gold - state['gold'] > 30: #melee bounty 36-40, ranged 42-48, siege 66-80
        if state['lh_creeps_history'] != []:
            state['lh_creeps_history'][-1].last_hit_success = True
    state['gold'] = gold
    # low priority actions
    if state['last_command'] == 'attack':
        if state['gold'] > 820:
            buy_item('phase boots')
            time.sleep(0.05)
            toggle('f3')
    # if state['last_command'] == 'last_hit':
    #     save_image(image, "last_hit_%s.png" % state['counter'])
    if code_interact:
        code.interact(local=dict(globals(), **locals()))


if __name__ == '__main__':
    t = time.time()
    time.sleep(6)
    state = initialize_state()
    startup(state)
    # time.sleep(60*4)
    # image = get_image()
    # print "getting radiant creeps"
    # print get_radiant_creeps(image, middle_area)
    # time.sleep(10)
    while time.time()-state['start_time'] < 5*60:
        midgame_iterate(state)
    # midgame_iterate(state, code_interact=True)
    state['dire_creeps_history'] += state['dire_creeps']
    state['rad_creeps_history'] += state['rad_creeps']
    say_in_chat(['-win']) # Remove when doing time optimization
    print "iteration complete"
    # print state['counter']
    print "fps:", state['counter']/(time.time()-state['start_time'])
    import pickle
    pickle.dump(state,open( "save.p", "wb"))
    # print "radiant creep history:", state['rad_creeps_history']
    # print "dire creep history:", state['dire_creeps_history']
    # save_image(image,'init_generic.png')
    # code.interact(local=locals())
