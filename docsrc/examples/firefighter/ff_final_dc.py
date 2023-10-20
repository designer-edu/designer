from designer import *
from dataclasses import dataclass
# Put imports at the top of the file
from random import randint

@dataclass
class World:
    copter: DesignerObject
    copter_speed: int
    drops: list[DesignerObject]
    fires: list[DesignerObject]
    score: int
    counter: DesignerObject


# Set initial speed of the copter
COPTER_SPEED = 5
# Set the speed of the water drops
WATER_DROP_SPEED = 5


def create_world() -> World:
    """ Create the world """
    return World(create_copter(), COPTER_SPEED, [], [], 0,
                 text("black", "0", 14, get_width()/2))


def create_copter() -> DesignerObject:
    """ Create the copter """
    copter = emoji("helicopter")
    copter.y = get_height() * (1 / 3)
    copter.flip_x = True
    copter.scale = 2
    return copter


def move_copter(world: World):
    """ Move the copter horizontally"""
    world.copter.x += world.copter_speed


def head_left(world: World):
    """ Make the copter start moving left """
    world.copter_speed = -COPTER_SPEED
    world.copter.flip_x = False


def head_right(world: World):
    """ Make the copter start moving right """
    world.copter_speed = COPTER_SPEED
    world.copter.flip_x = True


def bounce_copter(world: World):
    """ Handle the copter bouncing off a wall """
    if world.copter.x > get_width():
        head_left(world)
    elif world.copter.x < 0:
        head_right(world)


def flip_copter(world: World, key: str):
    """ Change the direction that the copter is moving """
    if key == "left":
        head_left(world)
    elif key == "right":
        head_right(world)


def create_water_drop() -> DesignerObject:
    """ Create a water drop"""
    return circle("blue", 10)


def drop_water(world: World, key: str):
    """ Drop water from directly below the copter when space is pressed. """
    if key == 'space':
        new_drop = create_water_drop()
        move_below(new_drop, world.copter)
        world.drops.append(new_drop)


def move_below(bottom: DesignerObject, top: DesignerObject):
    """ Move the bottom object to be below the top object """
    bottom.y = top.y + top.height/2
    bottom.x = top.x

def make_water_fall(world: World):
    """ Move all the water drops down """
    for drop in world.drops:
        drop.y += WATER_DROP_SPEED


def destroy_waters_on_landing(world: World):
    """ Destroy any water drops that have landed on the ground """
    kept = []
    for drop in world.drops:
        if drop.y < get_height():
            kept.append(drop)
        else:
            destroy(drop)
    world.drops = kept

def create_fire() -> DesignerObject:
    """ Create a small fire randomly on the screen """
    fire = emoji('🔥')
    fire.scale_x = .1
    fire.scale_y = .1
    fire.anchor = 'midbottom'
    fire.x = randint(0, get_width())
    fire.y = get_height()
    return fire

def make_fires(world: World):
    """ Create a new fire at random times, if there aren't enough fires """
    not_too_many_fires = len(world.fires) < 5
    random_chance = randint(0, 30) == 0
    if not_too_many_fires and random_chance:
        world.fires.append(create_fire())

def grow_fires(world: World):
    """ Make each fire get a little bit bigger """
    for fire in world.fires:
        fire.scale_x += .01
        fire.scale_y += .01


def there_are_big_fires(world: World) -> bool:
    """ Return True if there are any fires that are big """
    any_big_fires_so_far = False
    for fire in world.fires:
        any_big_fires_so_far = any_big_fires_so_far or fire.scale_x > 5
    return any_big_fires_so_far


def collide_water_fire(world: World):
    destroyed_fires = []
    destroyed_drops = []
    # Compare every drop to every fire
    for drop in world.drops:
        for fire in world.fires:
            # Check if there are any collisions between each pair
            if colliding(drop, fire):
                # Remember to remove this drop and fire
                destroyed_drops.append(drop)
                destroyed_fires.append(fire)
                # And increase our score accordingly
                world.score += 1
    # Remove any fires/drops that were identified as colliding
    world.drops = filter_from(world.drops, destroyed_drops)
    world.fires = filter_from(world.fires, destroyed_fires)


def filter_from(old_list: list[DesignerObject], elements_to_not_keep: list[DesignerObject]) -> list[DesignerObject]:
    new_values = []
    for item in old_list:
        if item in elements_to_not_keep:
            destroy(item)
        else:
            new_values.append(item)
    return new_values

def flash_game_over(world):
    """ Show the game over message """
    world.counter.text = "GAME OVER! Your score was " + str(world.score)


when("starting", create_world)
when("updating", move_copter)
when("updating", bounce_copter)
when("updating", make_water_fall)
when("updating", destroy_waters_on_landing)
when("updating", make_fires)
when("updating", grow_fires)
when('updating', collide_water_fire)
when(there_are_big_fires, flash_game_over, pause)
when("typing", flip_copter)
when('typing', drop_water)

start()



