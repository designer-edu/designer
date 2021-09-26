from designer import *
import random


def teleport_the_frog(world):
    if not random.randint(0, 5):
        world['frog']['x'] = random.randint(0, get_width())
        world['frog']['y'] = random.randint(0, get_height())


def spin_the_frog(world):
    world['frog']['angle'] = (world['frog']['angle'] + 10) % 360


def create_the_world():
    FROG_PICTURE = 'https://cdn.pixabay.com/photo/2017/08/15/15/44/frog-2644410_960_720.png'
    return {
        'frog': image(FROG_PICTURE, 0, 0, 200, 300)
    }


when('starting', create_the_world)
when('updating', teleport_the_frog, spin_the_frog)
draw()
