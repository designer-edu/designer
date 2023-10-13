from designer import *
from dataclasses import dataclass


# NOTE: Place these lines at the beginning, right after imports
# Set speed of the copter
COPTER_SPEED = 5


@dataclass
class World:
    copter: DesignerObject


def create_world() -> World:
    """ Create the world """
    return World(create_copter())


def create_copter() -> DesignerObject:
    """ Create the copter """
    copter = emoji("helicopter")
    copter.y = get_height() * (1 / 3)
    copter.flip_x = True
    return copter


# NOTE: Place this after your create_copter definition
def move_copter(world: World):
    """ Move the copter horizontally"""
    world.copter.x += COPTER_SPEED


when("starting", create_world)
# NOTE: Place this at the bottom, before start()
when("updating", move_copter)

start()

