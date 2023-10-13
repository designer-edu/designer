from designer import *
from dataclasses import dataclass


@dataclass
class World:
    copter: DesignerObject
    copter_speed: int


# Set initial speed of the copter
COPTER_SPEED = 5


def create_world() -> World:
    """ Create the world """
    return World(create_copter(), COPTER_SPEED)


def create_copter() -> DesignerObject:
    """ Create the copter """
    copter = emoji("helicopter")
    copter.y = get_height() * (1 / 3)
    copter.flip_x = True
    return copter


def move_copter(world: World):
    """ Move the copter horizontally"""
    world.copter.x += ___


def bounce_copter(world: World):
    """ Handle the copter bouncing off a wall """
    if world.copter.x > get_width():
        world.copter_speed = ___
    elif world.copter.x < 0:
        ___ = ___


when("starting", create_world)
when("updating", move_copter)
when("updating", bounce_copter)

start()

