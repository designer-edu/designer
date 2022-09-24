from designer import *
from dataclasses import dataclass
from math import sin, cos, degrees, radians
from random import randint

def ldx(d, l):
    return cos(radians(d)) * l

def ldy(d, l):
    return -sin(radians(d)) * l

@dataclass
class Tree:
    left: 'Tree'
    right: 'Tree'
    branch: DesignerObject

@dataclass
class World:
    tree: Tree

def build_tree(x: int, y: int, direction: int, length: int) -> Tree:
    if length < 1:
        return None
    tx = x + ldx(direction, length)
    ty = y + ldy(direction, length)
    branch = line('black', x, y, tx, ty, thickness=2)
    return Tree(build_tree(tx, ty, direction + randint(-30, 0), length /2),
                build_tree(tx, ty, direction + randint(0, 30), length /2),
                branch)

start(World(build_tree(get_width()//2, get_height()*3/4, 90, 200)))