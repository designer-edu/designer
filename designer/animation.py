import math

from designer.helpers import get_width, get_height
from designer.objects.designer_object import DesignerObject
import pygame
import designer
import random
from designer.utilities.animation import *
from designer.utilities.easings import Linear, Iterate, Random


def glide_around(obj, speed):
    """
    Moves object around at random.

    :param objects: Object to move around
    :type objects: DesignerObject or DesignerGroup
    :param speed: Pixels to move per second
    :type speed: int
    :return: None
    """
    obj.animate(Animation('x', Random(-speed, speed), 1, absolute=False, loop=True))
    obj.animate(Animation('y', Random(-speed, speed), 1, absolute=False, loop=True))


def glide_right(obj, speed):
    """
    Moves object to the right of the window.

    :param obj: Object to move
    :type obj: DesignerObject or DesignerGroup
    :param speed: Pixels to move per second
    :type speed: int
    :return: None
    """
    obj.animate(Animation('x', Linear(obj['x'], get_width()), get_width() / speed))


def glide_left(obj, speed):
    """
    Moves object to the left of the window.

    :param obj: Object to move
    :type obj: DesignerObject
    :param speed: Pixels to move per second
    :type speed: int
    :return: None
    """
    obj.animate(Animation('x', Linear(obj['x'], 0), obj['x'] / speed))


def glide_up(obj, speed):
    """
    Moves object up on the window.

    :param obj: Object to move
    :type obj: DesignerObject or DesignerGroup
    :param speed: Pixels to move per second
    :type speed: int
    :return: None
    """
    obj.animate(Animation('y', Linear(obj['y'], 0), obj['y']/speed))


def glide_down(obj, speed):
    """
    Moves object down on the window.

    :param obj: Object to move
    :type obj: DesignerObject or DesignerGroup
    :param speed: Pixels to move per second
    :type speed: int
    :return: None
    """
    obj.animate(Animation('y', Linear(obj['y'], get_height()), (get_height()-obj['y'])/speed))


def glide_in_degrees(obj, direction, speed):
    """
    Moves object a given number of degrees in that direction

    :param obj: Object to move
    :type obj: DesignerObject or DesignerGroup
    :param direction: Direction in degrees counterclockwise for object to move
    :type direction: int
    :param speed: Pixels to move per second
    :type speed: int
    :return: None
    """
    raise NotImplementedError("This function is not ready yet!")

def spin(obj, duration=5, angle_limit=360):
    """
    Rotates object in place for a given number of degrees

    :param obj: Object to move
    :type obj: DesignerObject or DesignerGroup
    :param angle_limit: Degrees to rotate object
    :type angle_limit: int
    :param speed: Pixels to move per second
    :type speed: int
    :return: None
    """
    if isinstance(obj, DesignerObject):
        obj.animate(Animation('angle', Linear(0, angle_limit), duration, loop=True))


def linear_animation(obj, property, start, end, duration, absolute=False, shift=False, loop=False):
    obj.animate(Animation(property, Linear(start, end), duration, absolute, shift, loop))


def sequence_animation(obj, property, items, duration, times=1, absolute=False, shift=False, loop=False):
    obj.animate(Animation(property, Iterate(items, times), duration, absolute, shift, loop))
