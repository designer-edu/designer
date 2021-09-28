from designer import *
import random

def warp(image: Image):
  image['x'], image['y'] = random.randint(0, get_width()), random.randint(0, get_height())


def teleport_the_frog(world):
    warp(world['frog'])


def spin_the_frog(world, key):
    if key == 'up':
      world['frog']['angle'] = (world['frog']['angle'] + 10) % 360
    elif key == 'down':
      world['frog']['angle'] = (world['frog']['angle'] - 10) % 360

def create_the_world():
    FROG_PICTURE = 'https://cdn.pixabay.com/photo/2017/08/15/15/44/frog-2644410_960_720.png'
    return {
        'frog': image(FROG_PICTURE, 0, 0, 200, 300),
        'targets': [warp(rectangle('red', 50, 50)) for _ in range(50)],
        'score': 0
    }

def score_the_frog(world):
    remaining_targets = []
    for target in world['targets']:
        if colliding(world['frog'], target):
          world['score'] += 1
          destroy(target) # <-- This is unexpected! But how else do we tell Designer that it's dead?
        else:
          remaining_targets.append(target)
    world['targets'] = remaining_targets

when('starting', create_the_world)
when('clicking', teleport_the_frog)
when('typing', spin_the_frog)
when('updating', score_the_frog)
draw()
