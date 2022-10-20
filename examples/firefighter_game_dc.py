from designer import *
from dataclasses import dataclass
from random import randint

@dataclass
class World:
    plane: DesignerObject
    plane_speed: int
    drops: list[DesignerObject]
    fires: list[DesignerObject]
    score: int
    counter: DesignerObject

# Set speed of the plane
PLANE_SPEED = 5

# Set speed of water drops
WATER_DROP_SPEED = 5


# Function that creates the world
def create_world() -> World:
    return World(create_plane(), PLANE_SPEED, [], [], 0,
                 text("black", "", 30, get_width() / 2, 15))


# Function that creates the plane
def create_plane() -> DesignerObject:
    plane = image("airplane.png")
    plane.scale = 0.2
    plane.y = get_height() * (1 / 3)
    plane.flip_x = True
    return plane


# Function that moves the plane
def move_plane(world: World):
    world.plane.x += world.plane_speed


# Function that makes the plane bounce of the walls
def bounce_plane(world: World):
    if world.plane.x > get_width():
        head_left(world)
    elif world.plane.x < 0:
        head_right(world)


# Helperfunction for hitting the left wall of the game
def head_left(world: World):
    world.plane_speed = -PLANE_SPEED
    world.plane.flip_x = False


# Helperfunction for hitting the left wall of the game
def head_right(world: World):
    world.plane_speed = PLANE_SPEED
    world.plane.flip_x = True


# Function that allows the player to control the direction of the plane
def flip_plane(world: World, key: str):
    if key == "left":
        head_left(world)
    elif key == "right":
        head_right(world)


# Function that creates water drops
def create_water_drop() -> DesignerObject:
    return circle("blue", 5)


# Function that allows the user to drop water
def drop_water(world: World, key: str):
    if key == "space":
        new_drop = create_water_drop()
        move_below(new_drop, world.plane)
        world.drops.append(new_drop)


# Funtion that moves the water drops below the plane
def move_below(bottom: DesignerObject, top: DesignerObject):
    bottom.y = top.y + top.height / 2
    bottom.x = top.x


# Function that makes the drops fall
def make_water_fall(world):
    for drop in world.drops:
        drop.y += WATER_DROP_SPEED


# Function that destroys all drops that reached the bottom of the screen
def destroy_waters_on_landing(world):
    kept = []
    for drop in world.drops:
        if drop.y < get_height():
            kept.append(drop)
        else:
            destroy(drop)
    world.drops = kept


# Function that creates the fires
def create_fire() -> DesignerObject:
    fire = image("fire.png")
    fire.scale_x = .1
    fire.scale_y = .1
    fire.anchor = "midbottom"
    fire.x = randint(0, get_width())
    fire.y = get_height()
    return fire


# Function that grows the fires
def grow_fire(world: World):
    for fire in world.fires:
        fire.scale_x += 0.003
        fire.scale_y += 0.003


# Function that actually makes fires
def make_fires(world: World):
    not_too_many_fires = len(world.fires) < 11
    if not_too_many_fires:
        world.fires.append(create_fire())


# Function that checks if any fire reached their original size
def there_are_big_fires(world) -> bool:
    any_big_fires_so_far = False
    for fire in world.fires:
        any_big_fires_so_far = any_big_fires_so_far or fire.scale_x > 1
    return any_big_fires_so_far


# Function that updates the text to the current score
def update_counter(world):
    world.counter.text = str(world.score)


# Function that removes all fires and waters that should be destroyed
def filter_from(old_list: list, elements_to_not_keep: list) -> list:
    new_values = []
    for item in old_list:
        if item in elements_to_not_keep:
            destroy(item)
        else:
            new_values.append(item)
    return new_values


# Function that determines which drops/fires should be destroyed and counts
# the score (how often drops collide with fires)
def collide_water_fire(world):
    destroyed_fires = []
    destroyed_drops = []
    for drop in world.drops:
        for fire in world.fires:
            if colliding(drop, fire):
                destroyed_drops.append(drop)
                destroyed_fires.append(fire)
                world.score += 1
    world.drops = filter_from(world.drops, destroyed_drops)
    world.fires = filter_from(world.fires, destroyed_fires)


# Function that prints the end score
def print_score(world):
    print("Your score was", world.score)


# Function that flashes a game over message
def flash_game_over(world):
    world.counter.text = "GAME OVER!"


when("starting", create_world)
when("updating", move_plane)
when("updating", bounce_plane)
when("typing", flip_plane)
when("typing", drop_water)
when("updating", make_water_fall)
when("updating", destroy_waters_on_landing)
when("updating", grow_fire)
when("updating", make_fires)
when("updating", update_counter)
when("updating", collide_water_fire)
when(there_are_big_fires, print_score, flash_game_over, pause)

start()
