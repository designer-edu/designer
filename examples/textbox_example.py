from designer import *
from dataclasses import dataclass

@dataclass
class World:
    textbox: text
    cursor: rectangle
    position: int


def create_world() -> World:
    initial_text = "Hello"
    world = World(text("black", initial_text, 40),
                  rectangle('black', 2, 50),
                  len(initial_text))
    world.cursor.x = world.textbox.x + world.textbox.width//2
    return world


def move_cursor(world: World, amount: int):
    world.position += amount
    width, height = world.textbox.estimate_size(world.textbox.text[:world.position])
    world.cursor.x = world.textbox.x + width - world.textbox.width//2


def enter_text(world: World, key: str, character: str):
    if key == 'backspace':
        existing = world.textbox.text
        index = world.position
        world.textbox.text = existing[:index-1] + existing[index:]
        move_cursor(world, -1)
    elif key == 'delete':
        existing = world.textbox.text
        index = world.position
        world.textbox.text = existing[:index] + existing[index+1:]
        move_cursor(world, 0)
    elif key == 'left':
        move_cursor(world, -1)
    elif key == 'right':
        move_cursor(world, 1)
    else:
        existing = world.textbox.text
        index = world.position
        world.textbox.text = existing[:index] + character + existing[index:]
        move_cursor(world, 1)

when('starting', create_world)
when('typing', enter_text)
debug()
