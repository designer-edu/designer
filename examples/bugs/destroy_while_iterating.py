from designer import *
from random import *

@starting
def create_world():
    return {
        'birds': [emoji("bird")],
        'timer': 0
    }

@updating
def tick_world(world):
    world['timer'] += 1

@typing
def remove_bird(world, key):
    if key == 'space':
        if world['birds']:
            destroy(world['birds'][0])
        world['birds'] = []

debug()