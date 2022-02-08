from designer import *
import math
import random

DECELERATION = .5

Spark = {'image': DesignerObject, 'velocity': float}

World = {'sparks': [Spark]}


def create_world() -> World:
    return {
        'sparks': []
    }


def create_spark(x: int, y: int) -> Spark:
    color = random.choice(['red', 'yellow', 'orange', 'blue', 'green', 'purple'])
    spark = circle(color, 5)
    # Partially transparent
    spark['alpha'] = .5
    # Rotate randomly 360 degrees
    spark['angle'] = random.randint(0, 360)
    # Move to the mouse location
    spark['x'] = x
    spark['y'] = y
    # Random velocity between 7 and 10
    velocity = random.randint(7, 10)
    return {'image': spark, 'velocity': velocity}


def make_sparks(world: World):
    # Get the current mouse x/y
    x = get_mouse_x()
    y = get_mouse_y()
    # Create spark at that location
    world['sparks'].append(create_spark(x, y))


def move_sparks(world: World):
    # For each spark
    for spark in world['sparks']:
        # Calculate their angle in radians (0 to 2pi)
        angle = math.radians(spark['image']['angle'])
        # Get the velocity
        velocity = spark['velocity']
        # Increase X by cosine of the angle times velocity
        spark['image']['x'] += math.cos(angle) * velocity
        # Decrease Y by sine of the angle times velocity
        spark['image']['y'] -= math.sin(angle) * velocity
        # Decrease velocity by the deceleration amount
        spark['velocity'] -= DECELERATION


def delete_stopped_sparks(world: World):
    kept = []
    for spark in world['sparks']:
        # Is the spark still moving?
        if spark['velocity'] > 0:
            # Keep this spark
            kept.append(spark)
        else:
            destroy(spark['image'])
    # Update sparks list
    world['sparks'] = kept


when('starting', create_world)
when('updating', make_sparks)
when('updating', move_sparks)
when('updating', delete_stopped_sparks)
start()
