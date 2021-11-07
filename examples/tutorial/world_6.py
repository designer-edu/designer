from designer import *
import random

# Define the shape of the World
World = {
    "box": DesignerObject,
    "message": DesignerObject,
    "score": int,
}


# Create a function that creates new worlds
def create_the_world() -> World:
    # Actually create an initial World instance
    return {
        # The world has a 20x30 black rectangle in it
        "box": rectangle("black", 200, 100),
        # The message to show the user
        "message": text("black", "Score:"),
        # The player's current score
        "score": 0
    }


# Define a function that spins the box
def spin_the_box(world: World):
    # Increase the boxes angle by one degree
    world['box']['angle'] += 1


# Move the box to a random position
def teleport_the_box(world: World):
    # Have a 1 in 10 chance of jumping around
    if random.randint(0, 9) == 0:
        # Set x/y to be random coordinates within the bounds of the
        # window, given by get_width() and get_height()
        world['box']['x'] = random.randint(0, get_width())
        world['box']['y'] = random.randint(0, get_height())


# Keep the message in sync with the current score
def track_the_score(world: World):
    # Get the current score
    score = world['score']
    # Update the message's text based on the score
    world['message']['text'] = "Score: " + str(score)


# Check if the box has been clicked and increase the score
def check_box_clicked(world: World, x: int, y: int):
    # Use the Designer function colliding to check if two objects or
    # an object and a point are colliding.
    if colliding(world['box'], x, y):
        # Update the score on a successful click
        world['score'] += 1


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
