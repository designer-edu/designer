from designer import *
from random import *

set_window_size(400, 100)


def make_orb():
    return rectangle("blue", 30, 30)


# def jiggle(orb):
#    orb['x'] += randint(-3, 3)

when('starting', make_orb)
# when('updating', jiggle)

start()