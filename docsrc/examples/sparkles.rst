
Sparkles
========

This game demonstrates how to have objects that:

* Have a velocity and deceleration
* Move at an angle using sine and cosine

.. code-block:: python

    from designer import *
    import math
    import random

    # Determines how fast the sparkles slow down
    DECELERATION = .5
    # Determines how big the spark is
    SPARK_SIZE = 5

    # Sparks are little circles with an angle and velocity
    Spark = {'image': DesignerObject, 'velocity': float}

    # The world is composed of sparks
    World = {'sparks': [Spark]}


    def create_world() -> World:
        """ Creates a world without any sparks """
        return {
            'sparks': []
        }


    def create_spark(x: int, y: int) -> Spark:
        """ Create a single spark of a rainbow color """
        # Pick a random color from among choices
        color = random.choice(['red', 'yellow', 'orange', 'blue', 'green', 'purple'])
        spark = circle(color, SPARK_SIZE)
        # Partially transparent
        spark['alpha'] = .5
        # Rotate randomly 360 degrees
        spark['angle'] = random.randint(0, 360)
        # Move to the mouse location
        spark['x'] = x
        spark['y'] = y
        # Random velocity between 7 and 10
        velocity = random.randint(7, 10)
        # Actually make the Spark
        return {'image': spark, 'velocity': velocity}


    def make_sparks(world: World):
        """ Make a new spark where ever the mouse is """
        # Get the current mouse x/y
        x = get_mouse_x()
        y = get_mouse_y()
        # Create spark at that location
        world['sparks'].append(create_spark(x, y))


    def move_sparks(world: World):
        """ Move each spark according to its velocity and angle """
        # For each spark
        for spark in world['sparks']:
            # Get the velocity
            velocity = spark['velocity']
            # Calculate their angle in radians (0 to 2pi)
            angle = math.radians(spark['image']['angle'])
            # Increase X by cosine of the angle times velocity
            spark['image']['x'] += math.cos(angle) * velocity
            # Decrease Y by sine of the angle times velocity
            spark['image']['y'] -= math.sin(angle) * velocity
            # Decrease velocity by the deceleration amount
            spark['velocity'] -= DECELERATION


    def delete_stopped_sparks(world: World):
        """ Filter out all sparks that aren't moving """
        kept = []
        # Go through all the sparks
        for spark in world['sparks']:
            # Is the spark still moving?
            if spark['velocity'] > 0:
                # Keep this spark
                kept.append(spark)
        # Update sparks list with our kept list
        world['sparks'] = kept

    # Bind the events
    when('starting', create_world)
    when('updating', make_sparks)
    when('updating', move_sparks)
    when('updating', delete_stopped_sparks)
    # Start the animation!
    start()
