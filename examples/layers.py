from designer import *
from dataclasses import dataclass

GRASS_SIZE = 50
INITIAL_GRASS_LIFE = 30 * 10


class Grass(rectangle):
    life: int


def create_grass() -> list[Grass]:
    grasses = []
    for x in range(0, get_width(), GRASS_SIZE):
        for y in range(0, get_height(), GRASS_SIZE):
            square = Grass("green", GRASS_SIZE, GRASS_SIZE,
                           x, y, life=INITIAL_GRASS_LIFE)
            square.anchor = 'topleft'
            square.layer = 'top'
            grasses.append(square)
    return grasses


when('starting', create_grass)
start()
