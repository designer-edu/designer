import math

from designer.utilities.vector import Vec2D
from designer.mouse import get_mouse_position


def move_forward(object, amount, angle=None):
    if angle is None:
        angle = object.angle
    object.x += math.cos(math.radians(angle)) * amount
    object.y -= math.sin(math.radians(angle)) * amount
    return object


def move_backward(object, amount, angle=None):
    if angle is None:
        angle = object.angle
    object.x -= math.cos(math.radians(angle)) * amount
    object.y += math.sin(math.radians(angle)) * amount
    return object


def turn_right(object, amount):
    object.angle -= amount
    return object


def turn_left(object, amount):
    object.angle += amount
    return object


def go_to_xy(object, x, y):
    object.x = x
    object.y = y
    return object


def go_to(object, other_object):
    object.x = other_object.x
    object.y = other_object.y
    return object


def go_to_mouse(object):
    object.x, object.y = get_mouse_position()
    return object


"""
TODO: `glide` versions of all of these

"""


def point_in_direction(object, angle):
    object.angle = angle
    return object


def angle_between(p1, p2):
    # https://stackoverflow.com/a/64807404/1718155
    d1 = p2[0] - p1[0]
    d2 = p2[1] - p1[1]
    if d1 == 0:
        if d2 == 0:  # same points?
            deg = 0
        else:
            deg = 90 if p1[1] > p2[1] else 270
    elif d2 == 0:
        deg = 0 if p1[0] < p2[0] else 180
    else:
        deg = math.atan(d2 / d1) / math.pi * 180
        lowering = p1[1] < p2[1]
        if (lowering and deg < 0) or (not lowering and deg > 0):
            deg += 180
        else:
            deg += 0
    return deg


def point_towards(object, other_object):
    object.angle = angle_between(object.pos, other_object.pos)
    return object


def point_towards_mouse(object):
    object.angle = angle_between(object.pos, get_mouse_position())
    return object


def change_x(object, amount):
    object.x += amount
    return object


def change_y(object, amount):
    object.y += amount
    return object


def change_xy(object, x_amount, y_amount):
    object.x += x_amount
    object.y += y_amount
    return object


def set_x(object, new_x):
    object.x = new_x
    return object


def set_y(object, new_y):
    object.y = new_y
    return object


def get_x(object):
    return object.x


def get_y(object):
    return object.y


def get_angle(object):
    return object.angle


def set_scale(object, scale):
    object.scale = scale
    return object


def grow(object, times):
    object.scale = times
    return object


def shrink(object, times):
    object.scale = 1/times
    return object


def change_scale(object, amount):
    object.scale += amount
    return object


def get_scale(object):
    return object.scale


def grow_x(object, amount):
    object.scale_x += amount
    return object


def grow_y(object, amount):
    object.scale.y += amount
    return object


def set_scale_x(object, scale):
    object.scale_x = scale
    return object


def set_scale_y(object, scale):
    object.scale_y = scale
    return object


def get_scale_x(object):
    return object.scale_x


def get_scale_y(object):
    return object.scale_y


def show(object):
    object.visible = True
    return object


def hide(object):
    object.visible = False
    return object


def set_visible(object, status):
    object.visible = status
    return object


def get_visible(object):
    return object.visible


def flip_x(object):
    object.flip_x = not object.flip_x
    return object


def flip_y(object):
    object.flip_y = not object.flip_y
    return object


def set_flip_x(object, new_flip_x):
    object.flip_x = new_flip_x
    return object


def set_flip_y(object, new_flip_y):
    object.flip_y = new_flip_y
    return object


def get_flip_x(object):
    return object.flip_x


def get_flip_y(object):
    return object.flip_y


move_to_xy = go_to_xy
move_to_x = set_x
move_to_y = set_y
move_to = go_to
move_to_mouse = go_to_mouse
