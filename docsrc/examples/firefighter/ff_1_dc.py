from dataclasses import dataclass
from designer import *


@dataclass
class World:
    pass


def create_world() -> World:
    """ Create the world """
    return World()


when('starting', create_world)
start()
