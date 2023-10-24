from designer import *
from dataclasses import dataclass
import math
import random


@dataclass
class World:
    avatar: DesignerObject
    speed: int
    direction: int
    obstacles: list[DesignerObject]


def move_random(obj: DesignerObject):
    """ Move the object to a random location """
    obj.x = random.randint(0, get_width())
    obj.y = random.randint(0, get_height())
    return obj


def create_world() -> World:
    """ Create the world """
    obstacles = [move_random(rectangle("black", 50, 50)) for _ in range(10)]
    dog = emoji("dog")
    for obstacle in obstacles:
        while colliding(obstacle, dog):
            move_random(obstacle)
    return World(dog, 5, 0, obstacles)


def move_avatar(world: World):
    """ Move the avatar horizontally"""
    angle = math.radians(world.direction)
    new_x = world.avatar.x + math.cos(angle) * world.speed
    new_y = world.avatar.y - math.sin(angle) * world.speed
    for obstacle in world.obstacles:
        if would_collide(world.avatar, new_x, new_y, obstacle):
            world.direction = random.randint(0, 360)
            angle = math.radians(world.direction)
            new_x = world.avatar.x + math.cos(angle) * world.speed
            new_y = world.avatar.y - math.sin(angle) * world.speed
    world.avatar.x = new_x
    world.avatar.y = new_y
    if world.avatar.x < 0 or world.avatar.x > get_width():
        world.direction = random.randint(0, 360)
    if not (0 < world.avatar.y < get_height()):
        world.direction = random.randint(0, 360)


when('starting', create_world)
when('updating', move_avatar)

start()