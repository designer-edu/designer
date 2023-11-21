from designer import *
from dataclasses import dataclass


@dataclass
class World:
    spinner: DesignerObject

def create_world() -> World:
    """ Create the world """
    spinner = emoji("dog")
    linear_animation(spinner, 'angle', 0, 360, 3, loop=True)
    sequence_animation(spinner, 'name', ['dog', 'cat', 'frog', 'dragon', 'sheep'], 5, loop=True)
    return World(spinner)


when('starting', create_world)
start()
