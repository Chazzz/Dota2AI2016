#!/usr/bin/python
# user_input.py
#
# Functions which involve keyboard or mouse inputs.
# Output is expected to be 100% side-effects.
#
# from user_input import (
#   left_click, 
#   right_click, 
#   toggle, 
#   move_camera, 
#   center_camera_on_hero, 
#   buy_item, 
#   sell_item_in_slot,
#   )

import uinput
import time
from PyQt4.QtGui import QCursor

STRING_MAP = {
    "a": uinput.KEY_A,
    "b": uinput.KEY_B,
    "c": uinput.KEY_C,
    "d": uinput.KEY_D,
    "e": uinput.KEY_E,
    "f": uinput.KEY_F,
    "g": uinput.KEY_G,
    "h": uinput.KEY_H,
    "i": uinput.KEY_I,
    "j": uinput.KEY_J,
    "k": uinput.KEY_K,
    "l": uinput.KEY_L,
    "m": uinput.KEY_M,
    "n": uinput.KEY_N,
    "o": uinput.KEY_O,
    "p": uinput.KEY_P,
    "q": uinput.KEY_Q,
    "r": uinput.KEY_R,
    "s": uinput.KEY_S,
    "t": uinput.KEY_T,
    "u": uinput.KEY_U,
    "v": uinput.KEY_V,
    "w": uinput.KEY_W,
    "x": uinput.KEY_X,
    "y": uinput.KEY_Y,
    "z": uinput.KEY_Z,
    "1": uinput.KEY_1,
    "2": uinput.KEY_2,
    "3": uinput.KEY_3,
    "4": uinput.KEY_4,
    "5": uinput.KEY_5,
    "6": uinput.KEY_6,
    "7": uinput.KEY_7,
    "8": uinput.KEY_8,
    "9": uinput.KEY_9,
    "0": uinput.KEY_0,
    "f1": uinput.KEY_F1,
    "f2": uinput.KEY_F2,
    "f3": uinput.KEY_F3,
    "f4": uinput.KEY_F4,
    "f5": uinput.KEY_F5,
    "f6": uinput.KEY_F6,
    "f7": uinput.KEY_F7,
    "f8": uinput.KEY_F8,
    "f9": uinput.KEY_F9,
    "f10": uinput.KEY_F10,
    "f11": uinput.KEY_F11,
    "f12": uinput.KEY_F12,
    "\t": uinput.KEY_TAB,
    "\n": uinput.KEY_ENTER,
    " ": uinput.KEY_SPACE,
    "space": uinput.KEY_SPACE,
    ".": uinput.KEY_DOT,
    ",": uinput.KEY_COMMA,
    "/": uinput.KEY_SLASH,
    "\\": uinput.KEY_BACKSLASH,
    "-": uinput.KEY_MINUS,
    "=": uinput.KEY_EQUAL,
    "esc": uinput.KEY_ESC,
}

DVORAK_MAP = {
    "a": uinput.KEY_A,
    "b": uinput.KEY_N,
    "c": uinput.KEY_I,
    "d": uinput.KEY_H,
    "e": uinput.KEY_D,
    "f": uinput.KEY_Y,
    "g": uinput.KEY_U,
    "h": uinput.KEY_J,
    "i": uinput.KEY_G,
    "j": uinput.KEY_C,
    "k": uinput.KEY_V,
    "l": uinput.KEY_P,
    "m": uinput.KEY_M,
    "n": uinput.KEY_L,
    "o": uinput.KEY_S,
    "p": uinput.KEY_R,
    "q": uinput.KEY_X,
    "r": uinput.KEY_O,
    "s": uinput.KEY_SEMICOLON,
    "t": uinput.KEY_K,
    "u": uinput.KEY_F,
    "v": uinput.KEY_DOT,
    "w": uinput.KEY_COMMA,
    "x": uinput.KEY_B,
    "y": uinput.KEY_T,
    "z": uinput.KEY_SLASH,
    "1": uinput.KEY_1,
    "2": uinput.KEY_2,
    "3": uinput.KEY_3,
    "4": uinput.KEY_4,
    "5": uinput.KEY_5,
    "6": uinput.KEY_6,
    "7": uinput.KEY_7,
    "8": uinput.KEY_8,
    "9": uinput.KEY_9,
    "0": uinput.KEY_0,
    "f1": uinput.KEY_F1,
    "f2": uinput.KEY_F2,
    "f3": uinput.KEY_F3,
    "f4": uinput.KEY_F4,
    "f5": uinput.KEY_F5,
    "f6": uinput.KEY_F6,
    "f7": uinput.KEY_F7,
    "f8": uinput.KEY_F8,
    "f9": uinput.KEY_F9,
    "f10": uinput.KEY_F10,
    "f11": uinput.KEY_F11,
    "f12": uinput.KEY_F12,
    "\t": uinput.KEY_TAB,
    "\n": uinput.KEY_ENTER,
    " ": uinput.KEY_SPACE,
    "space": uinput.KEY_SPACE,
    ".": uinput.KEY_E,
    ",": uinput.KEY_W,
    "/": uinput.KEY_BACKSLASH,
    "\\": uinput.KEY_BACKSLASH,
    "'": uinput.KEY_Q,
    "-": uinput.KEY_APOSTROPHE,
    "esc": uinput.KEY_ESC,
}

# TODO: Add Enchanted Mango! and so much more!
SHOP_DICT = {
    "clarity": ['q', '1'],
    "tango": ['q', '2'],
    "healing salve": ['q', '3'],
    "smoke of deceit": ['q', '4'],
    "town portal scroll": ['q', '5'],
    "dust of appearance": ['q', '6'],
    "animal courier": ['q', '9'], #add enchanted mango
    "flying courier": ['q', '8'],
    "observer ward": ['q', '9'],
    "sentry ward": ['q', '0'],
    "bottle": ['q', '-'],
    "iron branch": ['w', '1'],
    "gauntlets of strength": ['w', '2'],
    "slippers of agility": ['w', '3'],
    "mantle of intelligence": ['w', '4'],
    "circlet": ['w', '5'],
    "belt of strength": ['w', '6'],
    "band of elvenskin": ['w', '7'],
    "robe of the magi": ['w', '8'],
    "ogre club": ['w', '9'],
    "blade of alacrity": ['w', '0'],
    "staff of wizardry": ['w', '-'],
    "ultimate orb": ['w', '='],
    "ring of protection": ['e', '1'],
    "quelling blade": ['e', '2'],
    "stout shield": ['e', '3'],
    "blades of attack": ['e', '7'], #add orb of venom, blight stone
    "chainmail": ['e', '5'],
    "helm of iron will": ['e', '6'],
    "broadsword": ['e', '7'],
    "quarterstaff": ['e', '8'],
    "claymore": ['e', '9'],
    "javelin": ['e', '0'],
    "platemail": ['e', '-'],
    "mithril hammer": ['e', '='],
    "magic stick": ['r', '1'],
    "sage's mask": ['r', '2'],
    "ring of regen": ['r', '3'],
    "boots of speed": ['r', '4'],
    "gloves of haste": ['r', '5'],
    "cloak": ['r', '6'],
    "gem of true sight": ['r', '7'],
    "morbid mask": ['r', '8'],
    "ghost scepter": ['r', '9'],
    "talisman of evasion": ['r', '0'],
    "blink dagger": ['r', '-'],
    "shadow amulet": ['r', '='],
    "wraith band": ['a', '1'],
    "null talisman": ['a', '2'],
    "magic wand": ['a', '3'],
    "bracer": ['a', '4'],
    "poor man's shield": ['a', '5'],
    "soul ring": ['a', '6'],
    "phase boots": ['a', '7'],
    "power treads": ['a', '8'],
    "oblivion staff": ['a', '9'],
    "perseverance": ['a', '0'],
    "hand of midas": ['a', '-'],
    "boots of travel": ['a', '='],
    "ring of basilius": ['s', '1'],
    "headdress": ['s', '2'],
    "buckler": ['s', '3'],
    "urn of shadows": ['s', '4'],
    "ring of aquila": ['s', '5'],
    "tranquil boots": ['s', '6'],
    "medallion of courage": ['s', '7'],
    "arcane boots": ['s', '8'],
    "drum of endurance": ['s', '9'],
    "vladmir's offering": ['s', '0'],
    "mekansm": ['s', '-'],
    "pipe of insight": ['s', '='],
    "force staff": ['d', '1'],
    "necronomicon": ['d', '2'],
    "eul's scepter of divinity": ['d', '3'],
    "dagon": ['d', '4'],
    "veil of discord": ['d', '5'],
    "rod of atos": ['d', '6'],
    "aghanim's scepter": ['d', '7'],
    "orchid malevolence": ['d', '8'],
    "refresher orb": ['d', '9'],
    "scythe of vyse": ['d', '0'],
    "crystalys": ['f', '1'],
    "armlet of mordiggian": ['f', '2'],
    "skull basher": ['f', '3'],
    "shadow blade": ['f', '4'],
    "battle fury": ['f', '5'],
    "ethereal blade": ['f', '6'],
    "radiance": ['f', '7'],
    "monkey king bar": ['f', '8'],
    "daedalus": ['f', '9'],
    "butterfly": ['f', '0'],
    "divine rapier": ['f', '-'],
    "abyssal blade": ['f', '='],
    "hood of defiance": ['g', '1'],
    "blade mail": ['g', '2'],
    "vanguard": ['g', '3'],
    "soul booster": ['g', '4'],
    "black king bar": ['g', '5'],
    "shiva's guard": ['g', '6'],
    "manta style": ['g', '7'],
    "bloodstone": ['g', '8'],
    "linken's sphere": ['g', '9'],
    "assault cuirass": ['g', '0'],
    "heart of tarrasque": ['g', '-'],
    "crimson guard": ['g', '='],
    "helm of the dominator": ['h', '1'],
    "mask of madness": ['h', '2'],
    "sange": ['h', '3'],
    "yasha": ['h', '4'],
    "maelstrom": ['h', '5'],
    "diffusal blade": ['h', '6'],
    "desolator": ['h', '8'],
    "heaven's halberd": ['h', '8'],
    "sange and yasha": ['h', '9'],
    "mjollnir": ['h', '0'],
    "eye of skadi": ['h', '-'],
    "satanic": ['h', '='],
    "orb of venom": ['c', '1'],
    "ring of health": ['c', '2'],
    "void stone": ['c', '3'],
    "energy booster": ['c', '4'],
    "vitality booster": ['c', '5'],
    "point booster": ['c', '6'],
    "hyperstone": ['c', '7'],
    "demon edge": ['c', '8'],
    "mystic staff": ['c', '9'],
    "reaver": ['c', '0'],
    "eaglesong": ['c', '-'],
    "sacred relic": ['c', '='],
}

#TODO: Add ~.,/=-[]tab, see usr/include/linux/input.h
events = (
    uinput.KEY_A,
    uinput.KEY_B,
    uinput.KEY_C,
    uinput.KEY_D,
    uinput.KEY_E,
    uinput.KEY_F,
    uinput.KEY_G,
    uinput.KEY_H,
    uinput.KEY_I,
    uinput.KEY_J,
    uinput.KEY_K,
    uinput.KEY_L,
    uinput.KEY_M,
    uinput.KEY_N,
    uinput.KEY_O,
    uinput.KEY_P,
    uinput.KEY_Q,
    uinput.KEY_R,
    uinput.KEY_S,
    uinput.KEY_T,
    uinput.KEY_U,
    uinput.KEY_V,
    uinput.KEY_W,
    uinput.KEY_X,
    uinput.KEY_Y,
    uinput.KEY_Z,
    uinput.KEY_1,
    uinput.KEY_2,
    uinput.KEY_3,
    uinput.KEY_4,
    uinput.KEY_5,
    uinput.KEY_6,
    uinput.KEY_7,
    uinput.KEY_8,
    uinput.KEY_9,
    uinput.KEY_0,
    uinput.KEY_F1,
    uinput.KEY_F2,
    uinput.KEY_F3,
    uinput.KEY_F4,
    uinput.KEY_F5,
    uinput.KEY_F6,
    uinput.KEY_F7,
    uinput.KEY_F8,
    uinput.KEY_F9,
    uinput.KEY_F10,
    uinput.KEY_F11,
    uinput.KEY_F12,
    uinput.KEY_DOT,
    uinput.KEY_COMMA,
    uinput.KEY_SPACE,
    uinput.KEY_SLASH,
    uinput.KEY_BACKSLASH,
    uinput.KEY_TAB,
    uinput.KEY_ENTER,
    uinput.KEY_LEFTSHIFT,
    uinput.KEY_ESC,
    uinput.KEY_SEMICOLON,
    uinput.ABS_X,
    uinput.ABS_Y,
    uinput.REL_X,
    uinput.REL_Y,
    uinput.BTN_LEFT,
    uinput.BTN_RIGHT,
    uinput.BTN_MIDDLE,
    uinput.KEY_APOSTROPHE,
    uinput.KEY_LEFTBRACE,
    uinput.KEY_RIGHTBRACE,
    uinput.KEY_MINUS,
    uinput.KEY_EQUAL,
    uinput.KEY_UP,
    uinput.KEY_DOWN,
    uinput.KEY_LEFT,
    uinput.KEY_RIGHT,
    uinput.REL_WHEEL,
)

device = uinput.Device(events)
time.sleep(01) # Device has unfriendly race conditions

#TODO: Update automatically for 1440x2560 vs 1080x1920
screenx = 1920 #varies based on monitor size
screeny = 1080 #see above comment

def mousedemo():
    device.emit(uinput.REL_WHEEL, 1)
    time.sleep(1)
    device.emit(uinput.REL_WHEEL, -1)
    time.sleep(1)
    device.emit(uinput.REL_WHEEL, 1)
    print "complete"

def camera_drag_demo():
    device.emit(uinput.BTN_MIDDLE, 1)
    time.sleep(1)
    device.emit(uinput.REL_X, 200)
    device.emit(uinput.REL_Y, 200)
    time.sleep(1)
    device.emit(uinput.BTN_MIDDLE, 0)
    pass

def center_camera_on_hero():
    device.emit_click(uinput.KEY_F1)
    time.sleep(0.02) #minimum is 0.002
    device.emit_click(uinput.KEY_F1)
    # time.sleep(0.05) # time it takes after command to center camera

def calculate_camera_delay(dist):
    '''a camera accelerating from zero is similar to
    an object in free fall, in which case we use the integral of tanh(x)'''

def move_camera(x, y):
    '''move x then y'''
    raise Exception("not a complete function!!!")
    device.emit(key, 1)
    time.sleep(delay)
    device.emit(key, 0)
    time.sleep(0.25)

def clear_cursor():
    '''move cursor to top left of screen'''
    device.emit(uinput.REL_X, -screenx, syn = False)
    device.emit(uinput.REL_Y, -screeny)


def click_old(event, x, y, zeroed = False):
    # print x, y
    '''Don't import, use right_click and left_click instead'''
    # Go to top left of screen, move top coordinates, and click
    # clear_cursor()
    # time.sleep(0.2)
    if not zeroed:
        device.emit(uinput.REL_X, -screenx, syn = False)
        device.emit(uinput.REL_Y, -screeny)
    device.emit(uinput.REL_X, int(x), syn = False)
    device.emit(uinput.REL_Y, int(y))
    time.sleep(0.01)
    device.emit_click(event)

def click(event, x, y, tries=0):
    'use QCursor to lazily move mouse'
    pos = QCursor.pos()
    device.emit(uinput.REL_X, x-pos.x(), syn = False)
    device.emit(uinput.REL_Y, y-pos.y())
    newpos = QCursor.pos()
    if newpos.x() != x or newpos.y() != y:
        raise Exception("Failed to move to (%s, %s) on first try" % (x, y))
    time.sleep(0.01) #minimap misclick time
    device.emit_click(event)
    return 0

def left_click(x, y):
    return click(uinput.BTN_LEFT, x, y)

def right_click(x, y):
    return click(uinput.BTN_RIGHT, x, y)

def toggle(key):
    '''Press a key, to be used solo or with right/left_click'''
    device.emit_click(DVORAK_MAP[key])

def buy_item(item):
    device.emit_click(DVORAK_MAP['f4'])
    time.sleep(0.05)
    device.emit_click(DVORAK_MAP[SHOP_DICT[item][0]])
    time.sleep(0.05)
    device.emit_click(DVORAK_MAP[SHOP_DICT[item][1]])
    time.sleep(0.01)
    device.emit_click(DVORAK_MAP['f4'])
    time.sleep(0.01)

def sell_item_in_slot(slot):
    pass #need to fix inventorycoords

def level_up(key):
    device.emit_click(DVORAK_MAP['o'])
    time.sleep(0.05)
    device.emit_click(DVORAK_MAP[key])
    time.sleep(0.05)
    device.emit_click(DVORAK_MAP['esc'])
    time.sleep(0.05)

def say_in_chat(words, allchat = False):
    '''takes in list of strings and optional allchat argument'''
    if allchat:
        device.emit_combo([uinput.KEY_LEFTSHIFT, uinput.KEY_ENTER])
    else:
        device.emit_click(uinput.KEY_ENTER)
    time.sleep(0.2)
    for word in words:
        for letter in word:
            if letter == '_':
                device.emit_combo([uinput.KEY_LEFTSHIFT, DVORAK_MAP['-']])
                time.sleep(0.02)
            else:
                device.emit_click(DVORAK_MAP[letter])
                time.sleep(0.02)
        device.emit_click(uinput.KEY_SPACE)
        time.sleep(0.02)
    #determine whether time.sleep(0.002) is necessary
    if allchat:
        device.emit_combo([uinput.KEY_LEFTSHIFT, uinput.KEY_ENTER])
    else:
        device.emit_click(uinput.KEY_ENTER)
    time.sleep(0.1)