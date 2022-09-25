from designer import *
from dataclasses import dataclass


@dataclass
class KeyBox:
    """
    Keyboxes are a combo of the box itself, its text label, and its "active" status
    When you press the left/right keys, their box becomes active, indicating what
    direction the pair of boxes will move in.
    """
    box: DesignerObject
    text: DesignerObject
    active: bool


@dataclass
class World:
    """
    Worlds have a left and a right keybox
    """
    left: KeyBox
    right: KeyBox


BOX_SIZE = 60
BOX_SPEED = 5


def create_key_box(letter: str, x: int, y: int) -> KeyBox:
    """ Create a key box (combines its text, its box, and its current active status) """
    return KeyBox(rectangle('black', BOX_SIZE, BOX_SIZE, x, y, border=1),
                  text('black', letter, BOX_SIZE, x, y),
                  False)


def create_world() -> World:
    """ Create a left and right box """
    center_x = get_width() / 2
    center_y = get_height() / 2
    return World(create_key_box('<', center_x - BOX_SIZE / 2, center_y),
                 create_key_box('>', center_x + BOX_SIZE / 2, center_y))


def fill_key_box(key_box: KeyBox):
    """ Fill in the box with red, activate the box """
    key_box.box.color = 'red'
    key_box.box.border = None
    key_box.text.color = 'white'
    key_box.active = True


def empty_key_box(key_box: KeyBox):
    """ Restore the black border, deactivate the box """
    key_box.box.color = 'black'
    key_box.box.border = 1
    key_box.text.color = 'black'
    key_box.active = False


def press_key(world: World, key: str):
    """ When a key is pressed, activate the boxes """
    if key == 'left':
        fill_key_box(world.left)
    if key == 'right':
        fill_key_box(world.right)


def release_key(world: World, key: str):
    """ When a key is released, deactivate the boxes """
    if key == 'left':
        empty_key_box(world.left)
    if key == 'right':
        empty_key_box(world.right)


def handle_box_movement(world: World):
    """
    If the left key is active, move the boxes left.
    If the right key is active, move the boxes right.
    """
    if world.left.active:
        move_boxes(world, -BOX_SPEED)
    if world.right.active:
        move_boxes(world, BOX_SPEED)


def move_boxes(world: World, x_speed: int):
    """ Move both sets of boxes """
    move_box(world.left, x_speed)
    move_box(world.right, x_speed)


def move_box(key_box: KeyBox, x_speed: int):
    """ Move the X position of the box and its associated text """
    key_box.box.x += x_speed
    key_box.text.x += x_speed


when('starting', create_world)
when('typing', press_key)
when('done typing', release_key)
when('updating', handle_box_movement)
start()
