from designer import *
from random import randint

# world['box']['x'] = random.randint(0, get_width())
# world['box']['y'] = random.randint(0, get_height())
# World['box']['angle'] += 1

set_window_title(None)

NEW_FLAKE_CHANCE = 5  # percentage change of new flake on each update

Flake = {
    "fall_rate": int,
    "rotate_rate": int,
    "image": DesignerObject
}


def make_flake() -> Flake:
    return {"image": image("snowflakes/snow" + str(randint(0, 4)) + ".png", randint(0, get_width()), 0),
            "fall_rate": randint(1, 4),
            "rotate_rate": randint(0, 5)
            }


# Define the shape of the World
World = {
    "flakes": [Flake]
}


def make_world() -> World:
    # Actually create an initial World instance
    return {
        "flakes": make_flake_list(randint(4, 20))
    }


def make_flake_list(n: int) -> [Flake]:
    '''create a randonm list of n flakes'''
    flakes = []
    for i in range(n):
        flakes.append(make_flake())
    return flakes


def lower_flake(world: World):
    '''MAP template: lower every flake in list'''
    for flake in world["flakes"]:
        flake["image"]["y"] += flake["fall_rate"]


def rotate_flake(w: World):
    '''MAP template rotate every flake in list'''
    for flake in w["flakes"]:
        flake["image"]["angle"] += flake["rotate_rate"]


def add_new_flake(w: World):
    die = randint(1, 100)
    if die <= NEW_FLAKE_CHANCE:
        w["flakes"].append(make_flake())


def delete_old_flakes(w: World):
    '''delete flakes that are below the screen! Uses FILTER template'''
    new_flakes = []
    for flake in w["flakes"]:
        # doing this in parts so you see the idea
        y = flake["image"]["y"]  # y value of flake center
        top_y = y - (flake["image"]["height"] / 2)  # y value of the TOP of the flake
        if top_y <= get_height():
            new_flakes.append(flake)  # THEN this flake is still visible
        else:
            print("DELETE", flake['image']['y'], top_y, flake['image']['height'])
    w["flakes"] = new_flakes


when("starting", make_world)
when("updating", lower_flake)
when("updating", rotate_flake)
when("updating", add_new_flake)
when("updating", delete_old_flakes)
start()
