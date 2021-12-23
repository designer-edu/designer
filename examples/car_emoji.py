from designer import *


@starting
def create_car():
    return emoji("automobile", flip_x=True, x=64, scale=3)


@updating
def move_car(car):
    if car['x'] + car['width']/2 > get_width():
        car['flip_x'] = False
    elif car['x'] - car['width']/2 < 0:
        car['flip_x'] = True
    if car['flip_x']:
        car['x'] += 10
    else:
        car['x'] -= 10


start()
