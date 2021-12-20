from designer import *


SPACING = 36

LEVEL_DATA = [
    "🟥🟥🟥🟥🟥🟥🟥",
    "🟥     🟥",
    "🟥     🟥",
    "🟥     🟥",
    "🟥     🟥",
    "🟥     🟥",
    "🟥  😊  🟥",
    "🟥🟥🟥🟥🟥🟥🟥"
]

WIDTH = len(LEVEL_DATA[0])
HEIGHT = len(LEVEL_DATA)

def create_dinosaur():
    dino = emoji("T-rex")
    return {
        'image': dino,
        'v': 0,
        'h': 0
    }

def create_world():
    origin_x = get_width()//2 - WIDTH*SPACING//2
    origin_y = get_height()//2 - HEIGHT*SPACING//2
    return {
        'level': [
            emoji(character, origin_x + col * SPACING, origin_y + row * SPACING)
            for row, characters in enumerate(LEVEL_DATA)
            for col, character in enumerate(characters)
            if character != " "
        ],
        'dino': create_dinosaur()
    }

def not_hitting_ground(world):
    for box in world['level']:
        if colliding(box, world['dino']['image']):
            return False
    return True

def dino_falls(world):
    if world['dino']['v'] < 3:
        world['dino']['v'] += .1
    world['dino']['image']['y'] += world['dino']['v']

def dino_jump(world, key):
    if key == 'up':
        world['dino']['v'] = -2
        world['dino']['image']['y'] -= 5

def dino_walk(world, key):
    if key == 'left':
        world['dino']['image']['x'] -= 4
    if key == 'right':
        world['dino']['image']['x'] += 4

enable_keyboard_repeating()

when('starting', create_world)
when(not_hitting_ground, dino_falls)
when('typing', dino_jump, dino_walk)
start()