from designer import *
import random

def teleport_randomly(world):
    for obj in world.values():
        obj['x'] = random.randint(0, get_width())
        obj['y'] = random.randint(0, get_height())

def create_the_world():
    return {
        'box': rectangle('black', 25, 30),
        'orb': circle('red', 32),
        'ellipse': ellipse('blue', 50, 30),
        'arc': arc('green', 0, 90, 50, 30, thickness=3),
        'line': line('purple', 0, 0, 50, 75, 3),
        'text': text("yellow", "Hello There!")
    }

when('starting', create_the_world)
when('clicking', teleport_randomly)

start()