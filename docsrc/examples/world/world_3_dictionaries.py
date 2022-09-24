from designer import *

# Define the shape of the World
World = { "box": DesignerObject }

# Create a function that creates new worlds
def create_the_world() -> World:
    # Actually create an initial World instance
    return {
        # The world has a 20x30 black rectangle in it
        "box": rectangle("black", 200, 100)
    }

# Define a function that spins the box
def spin_the_box(world: World):
    # Increase the boxes angle by one degree
    world['box']['angle'] += 1

# This tells Designer to call our `create_the_world` function
# when the game starts, in order to setup our initial World.
when("starting", create_the_world)
# Tell Designer to call our spin_the_box function every update.
# There are usually 30 updates per second!
when("updating", spin_the_box)

start()