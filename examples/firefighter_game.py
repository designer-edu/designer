from designer import *
import random


def water_drop() -> DesignerObject:
    return circle("blue", 5)


def make_plane() -> DesignerObject:
    return rectangle("red", 20, 10)


def fire() -> DesignerObject:
    return image("https://cutewallpaper.org/21/fire-gif-transparent-background/Fireball-gif-transparent-clipart-images-gallery-for-free-.gif")


def place_randomly_on_bottom(obj):
    obj['x'] = random.randint(0, get_width())
    obj['y'] = get_height() - obj['height']
    return obj


def shrink(obj):
    obj['scale'] = .25
    return obj


def create_world():
    plane = make_plane()
    plane['hspeed'] = 1
    return {
        'fires': [place_randomly_on_bottom(shrink(fire())) for _ in range(10)],
        'drops': [],
        'plane': plane,
        'score': 0,
        'counter': text('black', '', 30)
    }

def move_plane(world):
    world['plane']['x'] += world['plane']['hspeed'] * 4
    if world['plane']['x'] < 0:
        world['plane']['hspeed'] *= -1
    elif world['plane']['x'] > get_width():
        world['plane']['hspeed'] *= -1

def flip_plane(world, key):
    if key == 'left':
        world['plane']['hspeed'] = -1
    elif key == 'right':
        world['plane']['hspeed'] = 1

def drop_water(world, key):
    print(key)
    if key == 32: #' ': #'space':
        new_drop = water_drop()
        move_below(new_drop, world['plane'])
        world['drops'].append(new_drop)

def move_below(bottom, top):
    bottom['y'] = top['y'] + top['height']
    bottom['x'] = top['x'] + top['width']/2 - bottom['width']/2
    return bottom

def drop_waters(world):
    kept = []
    for drop in world['drops']:
        drop['y'] += 4
        if drop['y'] < get_height():
            kept.append(drop)
        else:
            destroy(drop)
    world['drops'] = kept

def collide_water_fire(world):
    destroyed_fires = []
    destroyed_drops = []
    for drop in world['drops']:
        for fire in world['fires']:
            if colliding(drop, fire):
                if drop not in destroyed_drops:
                    destroyed_drops.append(drop)
                if fire not in destroyed_fires:
                    destroyed_fires.append(fire)
                    world['score'] += 1
    world['drops'] = [drop for drop in world['drops'] if drop not in destroyed_drops]
    world['fires'] = [fire for fire in world['fires'] if fire not in destroyed_fires]

def update_counter(world):
    world['counter'].text = str(world['score'])

when("starting", create_world)
when('typing', drop_water)
when('typing', flip_plane)
when('updating', move_plane)
when('updating', drop_waters)
when('updating', collide_water_fire)
when('updating', update_counter)
draw()
