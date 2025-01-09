from designer import *
from dataclasses import dataclass


@dataclass
class World:
    flashlight: DesignerObject
    timer: int


@starting
def create_world():
    flashlight = emoji("🔦", angle = 45, scale=.5)
    return World(flashlight=flashlight, timer=0)

@updating
def move_flashlight(world: World):
    if world.timer % 60 == 0:
        world.flashlight['flip_x'] = not world.flashlight['flip_x']
    world.timer = (world.timer + 1) % 60

start()