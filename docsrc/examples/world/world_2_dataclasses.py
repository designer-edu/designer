from designer import *
from dataclasses import dataclass

@dataclass
class World:
    box: DesignerObject


def create_the_world() -> World:
    """
    Create a new World with a 20x30 black rectangle inside.
    """
    return World(rectangle("black", 200, 100))

# This tells Designer to call our `create_the_world` function
# when the game starts, in order to setup our initial World.
when("starting", create_the_world)

start()