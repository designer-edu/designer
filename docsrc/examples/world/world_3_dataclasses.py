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

def spin_the_box(world: World):
    """
    Increase the world's box angle by one degree, spinning the box a small amount.
    """
    world.box.angle += 1

# This tells Designer to call our `create_the_world` function
# when the game starts, in order to setup our initial World.
when("starting", create_the_world)
# Tell Designer to call our spin_the_box function every update.
# There are usually 30 updates per second!
when("updating", spin_the_box)

start()