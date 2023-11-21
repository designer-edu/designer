from designer import *
from dataclasses import dataclass

@dataclass
class World:
    dog: DesignerObject
    cat: DesignerObject
    frog: DesignerObject
    dragon: DesignerObject
    sheep: DesignerObject

def create_world() -> World:
    """ Create the world """
    dog = emoji("dog")
    cat = emoji("cat")
    frog = emoji("frog")
    dragon = emoji("dragon")
    sheep = emoji("sheep")

    # Cat -> Frog -> Dog
    dog.layer = 'top'
    cat.layer = 'bottom'
    frog.pos = cat.pos = dog.pos = [get_width() / 3, get_height() / 3]
    cat.x -= 10
    dog.x += 10

    # Sheep and Dragon layered
    set_window_layers(['first', 'second'])
    sheep.layer = 'first'
    dragon.layer = 'second'

    return World(dog, cat, frog, dragon, sheep)

def swap_layers(world: World):
    """ Swap the layers of the dog and cat """
    world.dog.layer, world.cat.layer = world.cat.layer, world.dog.layer

    world.sheep.layer, world.dragon.layer = world.dragon.layer, world.sheep.layer

when('starting', create_world)
when('clicking', swap_layers)
start()