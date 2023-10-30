from designer import *
from dataclasses import dataclass


# Note that we have (Emoji) after the name of the new class!
class MovingEmoji(Emoji):
    """ An emoji that can move in a direction at a speed """
    speed: int
    direction: int

@dataclass
class World:
    dragon: MovingEmoji

def create_dragon() -> MovingEmoji:
    """ Create a dragon with initial speed 1, moving to the right"""
    return MovingEmoji('🐉', speed=1, direction=0)

def create_world() -> World:
    """ Create a world with a dragon in it """
    return World(create_dragon())

def accelerate_dragon(world: World, key: str):
    """ Pressing up or down increases or decreases the dragon's speed """
    if key == 'up':
        world.dragon.speed += 1
    elif key == 'down':
        world.dragon.speed -= 1

def spin_dragon(world: World, key: str):
    """ Pressing left or right increases or decreases the dragon's direction """
    if key == 'left':
        world.dragon.direction -= 10
    elif key == 'right':
        world.dragon.direction += 10

def move_dragon(world: World):
    """ Move the dragon forward in its current direction based on its speed """
    move_forward(world.dragon, world.dragon.speed, world.dragon.direction)

when('starting', create_world)
when('updating', move_dragon)
when('typing', spin_dragon)
when('typing', accelerate_dragon)
start()