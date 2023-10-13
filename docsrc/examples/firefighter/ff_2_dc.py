from designer import *
from dataclasses import dataclass


@dataclass
class World:
    copter: DesignerObject


def create_world() -> World:
    """ Create the world """
    return World(___)


def create_copter() -> DesignerObject:
    """ Create the copter """
    copter = emoji("helicopter")
    copter.y = get_height() * (1 / 3)
    copter.flip_x = True
    return copter


when("starting", create_world)

start()
