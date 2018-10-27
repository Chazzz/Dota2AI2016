#!/usr/bin/python
#
# Actor

# Strategy:
# Move to within range of dire creepwave, then stop
# For now, use move//center camera schema
# Observe creeps for one which is at last-hit threshold (5-10%)
# If so, attempt last-hit
# If no creeps in last-hit threshold,
# Check to see if there's any creeps about to enter last-hit threshold (10-20%)
# If so, recapture image, and recheck if it has crossed threshold
# Otherwise, look at radiant creeps, and make sure death is not imminent, moving back if necessary.

from get_image import get_image, save_image
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
    find_radiant_creeps,
    find_dire_creeps,
    get_levels_in_e,
    is_at_t2_5,
    get_attack_dmg,
    get_minimap_position,
    )
from creep_utils import (
    get_threshold_creeps,
    get_lowest_creep,
    percent_health_melee,
    percent_health_ranged,
    hero,
    )

import time
import random
import logging
import sys
import numpy as np #TODO: Remove on refactor

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

top_right_area = (1200, -1, 60, 675)
middle_area = (1000, 2200, 300, 900)

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
        'quick_fire_funs': [],
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
    right_click(96, 1348)
    time.sleep(10)
    center_camera_on_hero()
    time.sleep(0.1)
    say_in_chat(['-startgame'])
    time.sleep(3)
    state['start_time'] = time.time()

def log_action(state):
    logging.debug("%i:%0.2f %s" % (
        ((time.time()-state['start_time'])/60),
        (time.time()-state['start_time'])%60,
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
        time.sleep(0.1)
        left_click(360,1100)
        log_action(state)

def move_to_ancient(state):
    if state['last_command'] != 'forward':
        right_click(360,1100)
        state['last_command'] = 'forward'
        log_action(state)

def attack_t2(state):
    if state['last_command'] != 'attack_t2':
        toggle('a')
        time.sleep(0.1)
        left_click(280, 1180)
        state['last_command'] = 'attack_t2'
        log_action(state)

def move_to_mid_t3(state):
    if True: #state['last_command'] != 'retreat':
        right_click(96,1348)
        state['last_command'] = 'retreat'
        log_action(state)

def stop(state):
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
    right_click(creep.x+30,creep.y+60)
    state['last_command'] = 'last_hit'
    time.sleep(0.3) # Don't move while attacking
    clear_cursor()
    log_action(state)

def attack_creep_qf(state, creep):
    right_click(creep.x+30,creep.y+60, True)
    state['last_command'] = 'last_hit'
    time.sleep(0.3) # Don't move while attacking
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
    # print dire_creeps
    if dire_creeps:
        if len(dire_creeps) > 1:
            dmg_percent = percent_health_melee(state['hero_damage'])
            latency_percent = 0.0 #0.1
            soon_percent = 0.75 #percent_health_melee(state['hero_damage']) + 0.3
        else:
            dmg_percent = percent_health_ranged(state['hero_damage'])
            latency_percent = 0.0 #0.15
            soon_percent = 1 #percent_health_ranged(state['hero_damage']) + 0.5
        threshold_percent = dmg_percent+latency_percent
        lh_creeps = get_threshold_creeps(dire_creeps,
            (0.00,threshold_percent)
            )
        soon_lh_creeps = get_threshold_creeps(dire_creeps,
            (threshold_percent, soon_percent)
            )
        if lh_creeps:
            attack_creep(state, lh_creeps[0])
            return
        elif soon_lh_creeps:
            stop(state)
            clear_cursor()
            for creep in soon_lh_creeps:
                state['quick_fire_funs'].append(
                    gen_last_hit_quickfire(creep, (len(dire_creeps) > 1)))
            return
    else:
        attack_ancient(state)
        return

def get_num_buffer_creeps(rad_creeps):
    buffer_creeps = [creep for creep in rad_creeps if
        creep.x > 1200 and creep.y < 675]
    if len(buffer_creeps) > 1:
        return len(buffer_creeps)
    if len(buffer_creeps) == 1 and buffer_creeps[0].health > 0.9:
        return 1
    return 0

def get_num_backstab_creeps(dire_creeps):
    backstab_creeps = [creep for creep in dire_creeps if 
        creep.x < 1500 and creep.y > 400] # quadrant 3
    return len(backstab_creeps)

def in_range(dire_creeps):
    in_range_dist = 550
    lowest_creep = get_lowest_creep(dire_creeps)
    dist_to_creep = ((lowest_creep.x-hero.x)**2+(lowest_creep.y-hero.y)**2)**0.5
    return dist_to_creep < in_range_dist

def reposition(state, rad_creeps, dire_creeps, at_t2_5):
    '''transgress high ground iff creep buffer'''
    num_buffer_creeps = get_num_buffer_creeps(rad_creeps)
    if num_buffer_creeps > 1:
        last_hit(state, dire_creeps)
        if not state['quick_fire_funs']:
            long_iterate(state)
        return
    elif num_buffer_creeps == 1:
        attack_ancient(state)
        return
    else:
        if at_t2_5:
            move_to_mid_t3(state) # regress to hiding behind creeps, not 100% functional
            return
        elif not dire_creeps:
            if state['counter']%10 == 0:
                state['last_command'] = 'stop' # help with respawn
            attack_ancient(state)
            long_iterate(state) # comment out to help with t2.5 case
            return
        elif state['levels_in_e'] > 2 and not in_range(dire_creeps):
            attack_ancient(state)
            # long_iterate(state)
            return
        else:
            move_to_mid_t3(state)
            state['quick_fire_funs'].append(
                gen_retreat_quickfire(state['minimap_position']))
            return

def gen_last_hit_quickfire(creep, is_melee=True):
    area = [creep.x-25, creep.x+75, creep.y-15, creep.y+15]
    health_log = [creep.health]
    health_times = [time.time()]
    num_repeats = [0] # non-local
    hero_damage_fun = percent_health_melee
    if not is_melee:
        hero_damage_fun = percent_health_ranged
    def lh_area(state, img):
        dire_creeps = find_dire_creeps(img, area)
        if dire_creeps:
            for creep in dire_creeps:
                health_log.append(creep.health)
                health_times.append(time.time())
                # lose focus if there's a repeat
                if creep.health == health_log[-1]:
                    num_repeats[0] += 1
                else:
                    num_repeats[0] = 0
                if num_repeats[0] > 20:
                    # attack_creep_qf(state, creep)
                    # num_repeats[0] = 0
                    print "allowable repeats exceeded"
                    print health_log
                    return False
                # anticipate damage based on creeps with 1 attack/sec
                dh = []
                dt = []
                health_time = [time.time()-t for t in health_times]
                for i in range(len(health_log)-1):
                    dh.append(health_log[i]-health_log[i+1])
                    dt.append((health_time[i], health_time[i+1]))
                expected_damage = 0
                for i in range(len(dh)):
                    if dt[i][1] > 0.7 and dt[i][0] < 1:
                        expected_damage += dh[i]
                if creep.health-expected_damage < hero_damage_fun(state['hero_damage']):
                    attack_creep_qf(state, creep)
                    print "melee,", str(is_melee)
                    print (creep.x, creep.y)
                    print health_log
                    print health_times
                    print dh
                    print dt
                    print creep.health
                    return False
            return True
        else:
            print "creep missed"
            print health_log
            # print health_times
            return False
    return lh_area

def gen_retreat_quickfire(minimap_position):
    old_minimap_position = minimap_position
    def qf_retreat(state, image):
        '''
        move if haven't moved from original position
        otherwise, stop when no nearby enemies
        '''
        center_camera_on_hero()
        new_minimap_position = get_minimap_position(image)
        if np.all(np.isclose(old_minimap_position,new_minimap_position,atol=1)):
            move_to_mid_t3(state)
            return True
        dire_creeps = find_dire_creeps(image, middle_area)
        if not dire_creeps:
            stop(state)
        return dire_creeps
    return qf_retreat

def execute_quickfire_functions(state, img):
    '''re-evaluate quick_fire_funs, discarding irrelevant actions'''
    new_quickfire_funs = []
    for fun in state['quick_fire_funs']:
        if fun(state, img):
            new_quickfire_funs.append(fun)
    state['quick_fire_funs'] = new_quickfire_funs
    return

def midgame_iterate(state):
    state['counter'] += 1
    if not state['quick_fire_funs'] and (
        state['counter'] % 4 == 0 or state['last_command'] == 'retreat'):
        center_camera_on_hero()
        # time.sleep(0.2) # time it takes after command to center camera
    image = get_image()
    if state['quick_fire_funs']:
        execute_quickfire_functions(state, image)
        return
    # if state['save_counter'] == 200:
    #     save_image(image, '100.png')
    # if state['counter'] % 20 = 0:
    state['hero_damage'] = get_attack_dmg(image)
    state['levels_in_e'] = get_levels_in_e(image)
    state['minimap_position'] = get_minimap_position(image)
    if state['levels_in_e'] == 4:
        dire_creeps = find_dire_creeps(image, middle_area)
    else:
        dire_creeps = find_dire_creeps(image, top_right_area)
    # if get_num_backstab_creeps(dire_creeps): # when pushing t4s/ancient
    #     move_to_mid_t3(state)
    #     # Can't add qf function because breaks too many unittests :(
    #     state['quick_fire_funs'].append(
    #         gen_retreat_quickfire(state['minimap_position']))
    #     # time.sleep(2)
    #     return
    at_t2_5 = is_at_t2_5(image)
    # if not dire_creeps:
    #     bad_iterate(state)
    #     return
    # elif levels_in_e > 2 and not in_range(dire_creeps):
    #     bad_iterate(state)
    #     return
    rad_creeps = find_radiant_creeps(image, top_right_area)
    reposition(state, rad_creeps, dire_creeps, at_t2_5)

if __name__ == '__main__':
    t = time.time()
    time.sleep(6)
    state = initialize_state()
    startup(state)
    while time.time()-t < 1.4*60:
        midgame_iterate(state)
    say_in_chat(['-win']) # Remove when doing time optimization
    print "iteration complete"
    print state['counter']
    print state['counter']/(time.time()-state['start_time'])