from designer import *
import random
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

def teleport_the_box(world: World):
    """
    Move the box to a random position
    """
    # Have a 1 in 10 chance of jumping around
    if random.randint(0, 9) == 0:
        # Set x/y to be random coordinates within the bounds of the
        # window, given by get_width() and get_height()
        world.box.x = random.randint(0, get_width())
        world.box.y = random.randint(0, get_height())

# This tells Designer to call our `create_the_world` function
# when the game starts, in order to setup our initial World.
when("starting", create_the_world)
# Tell Designer to call our spin_the_box function every update.
# There are usually 30 updates per second!
when("updating", spin_the_box)
# Tell Designer to call teleport_the_box every update.
when("updating", teleport_the_box)

start()