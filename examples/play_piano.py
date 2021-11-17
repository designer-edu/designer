from designer import *

PIANO_NOTE = [
    'A1vL.wav',
    'A1vH.wav',
    'B1vH.wav',
    'C1vL.wav',
    'C1vH.wav',
    'D#1vL.wav',
    'D#1vH.wav',
    'F#1vL.wav',
    'F#1vH.wav'
]
KEYS = 9

WIDTH = get_width() / KEYS

def create_world():
    return {
        'filling': [
            rectangle('white', WIDTH - 10-6, 200-6, (x + .5) * WIDTH, get_height() / 2)
            for x in range(KEYS)
        ],
        'keys': [
            rectangle('black', WIDTH-10, 200, (x+.5)*WIDTH, get_height()/2, border=3)
            for x in range(KEYS)
        ],
    }


def handle_mouse(world):
    for key in world['filling']:
        if colliding(key, get_mouse_x(), get_mouse_y()):
            key['color'] = 'yellow'
        else:
            key['color'] = 'white'


def press_key(world, x, y):
    top_x = get_height() / 2 - 100
    bottom_x = get_height() / 2 + 100
    if top_x <= get_mouse_y() <= bottom_x:
        i = int(get_mouse_x() / WIDTH)
        #world['keys'][i]['color'] = 'red'
        play_sound('piano/'+PIANO_NOTE[i])



when('starting', create_world)
when('updating', handle_mouse)
when('clicking', press_key)

start()