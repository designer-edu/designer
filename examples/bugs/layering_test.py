from designer import *


@starting
def create_world():
    return {
        'banana': emoji("banana", layer="fruit"),
        'apple': emoji("red apple", layer="fruit"),
        "orange": emoji("tangerine", layer="fruit"),
        "potato": change_y(emoji("potato", layer="vegetable"), 20)
    }

@typing
def change_layer(world, key):
    if key in ('o', 'a', 'b'):
        if key == 'o':
            top, bottoms = 'orange', ('apple', 'banana')
        elif key == 'a':
            top, bottoms = 'apple', ('orange', 'banana')
        else:
            top, bottoms = 'banana', ('apple', 'orange')
        world[top]['layer'] = 'fruit:top'
        for bottom in bottoms:
            world[bottom]['layer'] = 'fruit:bottom'
    elif key == 'space':
        print(get_window_layers())
        for obj in world.values():
            print(repr(obj), obj.layer, obj._computed_layer)


set_window_layers(['vegetable', 'fruit'])

start()
