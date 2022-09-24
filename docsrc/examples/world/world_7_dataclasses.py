from designer import *
import random
from dataclasses import dataclass

@dataclass
class World:
    box: DesignerObject
    message: DesignerObject
    score: int


def create_the_world() -> World:
    """
    Create a new World with a 20x30 black rectangle inside, a message with default text,
    and a score that's initially 0.
    """
    return World(rectangle("black", 200, 100),
                 text("black", "Score:"),
                 0)

def spin_the_box(world: World):
    """
    Increase the world's box angle by one degree, spinning the box a small amount.
    """
    world.box.angle += 1

def teleport_the_box(world: World):
    """ Move the box to a random position """
    # Have a 1 in 10 chance of jumping around
    if random.randint(0, 9) == 0:
        # Set x/y to be random coordinates within the bounds of the
        # window, given by get_width() and get_height()
        world.box.x = random.randint(0, get_width())
        world.box.y = random.randint(0, get_height())

def track_the_score(world: World):
    """ Keep the message in sync with the current score """
    # Get the current score
    score = world.score
    # Update the message's text based on the score
    world.message.text = "Score: " + str(score)


def check_box_clicked(world: World, x: int, y: int):
    """ Check if the box has been clicked and increase the score """
    # Use the Designer function colliding to check if two objects or
    # an object and a point are colliding.
    if colliding(world.box, x, y):
        # Update the score on a successful click
        world.score += 1


# This tells Designer to call our `create_the_world` function
# when the game starts, in order to setup our initial World.
when("starting", create_the_world)
# Tell Designer to call our spin_the_box function every update.
# There are usually 30 updates per second!
when("updating", spin_the_box)
# Tell Designer to call teleport_the_box every update.
when("updating", teleport_the_box)
# Tell Designer to call track_the_score every update.
when("updating", track_the_score)
# Tell Designer to call check_box_clicked when the mouse is clicked
when('clicking', check_box_clicked)

start()