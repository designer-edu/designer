from random import randint
from designer import *


def warp(obj):
    obj['x'] = randint(0, get_width())
    obj['y'] = randint(0, get_height())
    return obj


def red_dot():
    return circle("red", 10)


def create_world():
    return {
        'dots': [warp(red_dot()) for _ in range(50)],
        'score': 0,
        'message': text('black', "", 16)
    }


def grab_dots(world, x, y):
    kept_dots = []
    for dot in world['dots']:
        if colliding(dot, x, y):
            dot.kill()
            world['score'] += 1
        else:
            kept_dots.append(dot)
    world['dots'] = kept_dots


def update_score(world):
    new_text = "Score: " + str(world['score']) + ", Dots: " + str(len(world['dots']))
    world['message']['text'] = new_text


when('starting', create_world)
when('clicking', grab_dots)
when('updating', update_score)

draw()
