from designer import *
from dataclasses import dataclass


@dataclass
class World:
    copter: DesignerObject
    copter_speed: int
    drops: list[DesignerObject]


# Set initial speed of the copter
COPTER_SPEED = 5


def create_world() -> World:
    """ Create the world """
    return World(create_copter(), COPTER_SPEED, [])


def create_copter() -> DesignerObject:
    """ Create the copter """
    copter = emoji("helicopter")
    copter.y = get_height() * (1 / 3)
    copter.flip_x = True
    return copter


def move_copter(world: World):
    """ Move the copter horizontally"""
    world.copter.x += ___


def head_left(world: World):
    """ Make the copter start moving left """
    world.copter_speed = -COPTER_SPEED
    world.copter.flip_x = False


def head_right(world: World):
    """ Make the copter start moving right """
    world.copter_speed = COPTER_SPEED
    world.copter.flip_x = True


def bounce_copter(world: World):
    """ Handle the copter bouncing off a wall """
    if world.copter.x > get_width():
        head_left(world)
    elif world.copter.x < 0:
        head_right(world)


def flip_copter(world: World, key: str):
    """ Change the direction that the copter is moving """
    if key == "left":
        ___
    elif key == "right":
        ___


def create_water_drop() -> DesignerObject:
    """ Create a water drop"""
    return circle("blue", ___)


def drop_water(world: World, key: str):
    """ Create a water drop when the space bar is pressed """
    if key == 'space':
        new_drop = create_water_drop()
        world.___.append(___)


def move_below(bottom: DesignerObject, top: DesignerObject):
    """ Move the bottom object to be below the top object """
    bottom.y = ___.y + ___.height/2
    bottom.y = ___.x


when("starting", create_world)
when("updating", move_copter)
when("updating", bounce_copter)
when("___", flip_copter)
when('typing', drop_water)

start()

