from designer import *


enable_keyboard_repeating()

def create_world():
    return {
        'circle': circle('red', 100),
        'repeating': True
    }

def handle_keyboard(world, key):
    if key == 'left':
        world['circle']['x'] -= 10
    elif key == 'right':
        world['circle']['x'] += 10
    elif key == 'space':
        if world['repeating']:
            disable_keyboard_repeating()
            world['circle']['color'] = 'blue'
        else:
            enable_keyboard_repeating()
            world['circle']['color'] = 'red'
        world['repeating'] = not world['repeating']

when('starting', create_world)
when('typing', handle_keyboard)

start()