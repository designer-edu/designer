from designer import *
import random
from designer.objects.image import Image

WATER_DROP_SPEED = 5
PLANE_SPEED = 5

set_window_title(None)

World = {
    'fires': [DesignerObject],
    'drops': [DesignerObject],
    'plane': DesignerObject,
    'score': int,
    'counter': DesignerObject
}


def create_world():
    plane = create_plane()
    return {
        'fires': [],
        'drops': [],
        'plane': plane,
        'score': 0,
        'counter': text('black', '', 30, get_width() / 2, 100)
    }


def create_water_drop() -> DesignerObject:
    return circle("blue", 5)


def create_plane() -> DesignerObject:
    plane = image("airplane.png")
    plane['scale'] = .25
    plane['hspeed'] = PLANE_SPEED
    return plane


def create_fire(size=.1) -> DesignerObject:
    fire = image('fire.png', anchor="midbottom", scale=.1)
    fire['x'] = random.randint(0, get_width())
    fire['y'] = get_height()
    fire['scale_y'] = size
    return fire


def go_right(plane):
    plane['hspeed'] = PLANE_SPEED
    plane['flip_x'] = False


def go_left(plane):
    plane['hspeed'] = -PLANE_SPEED
    plane['flip_x'] = True


def move_plane(world):
    world['plane']['x'] += world['plane']['hspeed']
    if world['plane']['x'] < 0:
        go_right(world['plane'])
    elif world['plane']['x'] > get_width():
        go_left(world['plane'])


def flip_plane(world, key):
    if key == 'left':
        go_left(world['plane'])
    elif key == 'right':
        go_right(world['plane'])


def drop_water(world, key):
    if key == 'space':
        new_drop = create_water_drop()
        move_below(new_drop, world['plane'])
        world['drops'].append(new_drop)


def move_below(bottom, top):
    bottom['y'] = top['y'] + top['height']/2
    bottom['x'] = top['x']


def drop_waters(world):
    kept = []
    for drop in world['drops']:
        drop['y'] += WATER_DROP_SPEED
        if drop['y'] < get_height():
            kept.append(drop)
        else:
            destroy(drop)
    world['drops'] = kept


def filter_from(values, from_list):
    result = []
    for value in values:
        if value not in from_list:
            result.append(value)
    return result


def collide_water_fire(world):
    destroyed_fires = []
    destroyed_drops = []
    for drop in world['drops']:
        for fire in world['fires']:
            if colliding(drop, fire):
                if drop not in destroyed_drops:
                    destroyed_drops.append(drop)
                    destroy(drop)
                if fire not in destroyed_fires:
                    destroyed_fires.append(fire)
                    destroy(fire)
                    world['score'] += 1
    world['drops'] = filter_from(world['drops'], destroyed_drops)
    world['fires'] = filter_from(world['fires'], destroyed_fires)


def update_counter(world):
    world['counter']['text'] = str(world['score'])


def grow_fire(world):
    for fire in world['fires']:
        fire['scale'] += .0001 * (1 + world['score'])
    if len(world['fires']) < 8 and not random.randint(0, 10 * len(world['fires'])):
        new_fire = create_fire()
        linear_animation(new_fire, 'alpha', 0, 1.0, 3)
        world['fires'].append(new_fire)


def there_are_big_fires(world):
    any_big_fires_so_far = False
    for fire in world['fires']:
        any_big_fires_so_far = any_big_fires_so_far or fire['scale_x'] >= 1
    return any_big_fires_so_far


def print_score(world):
    print("Your score was", world['score'])


def flash_game_over(world):
    world['counter']['text'] = "GAME OVER!"


when("starting", create_world)
when('updating', move_plane)
when('updating', drop_waters)
when('updating', grow_fire)
when('updating', collide_water_fire)
when('updating', update_counter)
when('typing', drop_water)
when('typing', flip_plane)
when(there_are_big_fires, print_score, flash_game_over, pause)
start()
