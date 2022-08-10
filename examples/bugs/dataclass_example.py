from designer import *
from dataclasses import dataclass
from random import randint

@dataclass
class Dog:
    picture: DesignerObject
    label: DesignerObject

@dataclass
class Zoo:
    dogs: list[Dog]
    cat: DesignerObject

@dataclass
class World:
    animals: Zoo
    timer: int


def create_world() -> World:
    return World(Zoo([], emoji("cat")), 0)

@updating
def scatter_animals(world: World):
    for dog in world.animals.dogs:
        if colliding(dog.picture, world.animals.cat):
            scatter_dog(dog)
        for other_dog in world.animals.dogs:
            if other_dog != dog and colliding(other_dog.picture, dog.picture):
                scatter_dog(other_dog)
                scatter_dog(dog)


def scatter_dog(dog: Dog):
    hspeed = randint(-5, 5)
    vspeed = randint(-5, 5)
    dog.picture.x += hspeed
    dog.picture.y += vspeed
    dog.label.x = dog.picture.x
    dog.label.y = dog.picture.y
    #dog.picture.flip_x = hspeed > 0
    #dog.picture.angle = vspeed*3

@updating
def add_dogs(world: World):
    world.timer += 1
    if world.timer % 45 == 0:
        dog_count = str(len(world.animals.dogs))
        dog_text = text("black", dog_count, layer=":above")
        world.animals.dogs.append(Dog(emoji("dog"), dog_text))


when('starting', create_world)

debug()