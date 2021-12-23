import math
from designer import *
import random

set_window_title(None)

def warp(obj):
    obj['x'] = random.randint(0, get_width())
    obj['y'] = random.randint(0, get_height())
    return obj


def in_bounds(obj):
    return 0 <= obj['x'] <= get_width() and 0 <= obj['y'] <= get_height()


def jiggle_the_ada(world):
    ada = world['ada']
    ada['hspeed'] = max(-ZOOMIES, min(ZOOMIES, ada['hspeed'] + random.random() - .5))
    ada['vspeed'] = max(-ZOOMIES, min(ZOOMIES, ada['vspeed'] + random.random() - .5))
    ada['x'] += ada['hspeed']
    ada['y'] += ada['vspeed']
    if not in_bounds(ada):
        warp(ada)
        ada['hspeed'] = 0
        ada['vspeed'] = 0


def spin_the_ada(world):
    pass
    # world['ada']['angle'] = (world['ada']['angle'] + 10) % 360


COLORS = ['red', 'green', 'purple']

hidden_box1 = warp(rectangle('green', 30, 50))

# hidden_box2
warp(rectangle('blue', 30, 50))

@when('input.keyboard.u')
def activate_hidden_box(world):
    if hidden_box1.active:
        destroy(hidden_box1)
    else:
        hidden_box1._reactivate()
    print({n: [h0[0].__self__ for h0 in h if hasattr(h0[0], '__self__')] for n, h in get_director().current_window._handlers.items()})


def create_the_world():
    # This will not persist, it was not saved in the world!
    text("black", "Creating the world", 30)
    return {
        'orbs': [make_orb() for i in range(5)],
        'ada': make_ada(),
        'box': warp(rectangle('orange', 30, 50))
    }


ZOOMIES = 6


def make_ada():
    FROG_PICTURE = 'https://cdn.pixabay.com/photo/2017/08/15/15/44/ada-2644410_960_720.png'
    # image(FROG_PICTURE, 0, 0, 200, 300)
    # ada = circle('blue', 50)
    ada = image("ada.png")
    ada['hspeed'] = random.randint(-ZOOMIES, ZOOMIES)
    ada['vspeed'] = random.randint(-ZOOMIES, ZOOMIES)
    ada['scale'] = .25
    return ada


def make_orb():
    orb = warp(circle(random.choice(COLORS), 10))
    orb['direction'] = random.randint(0, 360)
    orb['speed'] = random.randint(1, 4)
    orb['slobber'] = 0
    return orb


def warp_the_orbs(world):
    for orb in world['orbs']:
        warp(orb)


def color_cycle(a_color: str) -> str:
    return ('red' if a_color == 'purple' else
            'green' if a_color == 'red' else
            'purple')


def recolor_the_orbs(world, key, unicode):
    for orb in world['orbs']:
        if unicode == ' ':
            orb['color'] = color_cycle(orb['color'])
        elif unicode == 'b':
            orb['scale'] = orb['scale'] + .1
        elif unicode == 's':
            orb['scale'] = orb['scale'] - .1


def step_orbs(world):
    for orb in world['orbs']:
        orb['x'] += math.cos(math.degrees(orb['direction'])) * orb['speed']
        orb['y'] += math.sin(math.degrees(orb['direction'])) * orb['speed']
        if orb['x'] < 0:
            orb['x'] = get_width()
        elif orb['x'] > get_width():
            orb['x'] = 0
        if orb['y'] < 0:
            orb['y'] = get_height()
        elif orb['y'] > get_height():
            orb['y'] = 0
        if colliding(orb, world['ada']):
            orb['speed'] *= -1
            orb['slobber'] += 1
            orb['scale'] *= .99
            world['ada']['hspeed'] *= .99
            world['ada']['vspeed'] *= .99
            world['ada']['angle'] = random.randint(-5, 5)
        elif orb['scale'][0] < 1:
            orb['scale'] += .0001


def eat_the_orbs(world):
    kept_orbs = []
    for orb in world['orbs']:
        if orb['scale'][0] >= .5:
            kept_orbs.append(orb)
        else:
            destroy(orb)
    world['orbs'] = kept_orbs


def destroy_latest_orb(world, key):
    if key == 'd':
        if world['orbs']:
            world['orbs'].pop().destroy()
        else:
            world['orbs'].append(make_orb())

when('starting', create_the_world)
when('updating', jiggle_the_ada, spin_the_ada, step_orbs, eat_the_orbs)
when('clicking', warp_the_orbs)
when('typing', recolor_the_orbs, destroy_latest_orb)
draw()
