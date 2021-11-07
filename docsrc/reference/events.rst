.. _event:

List of Events
--------------

These are functions you can define and then bind using the :ref:`when<when>` function.

`starting`
==========

The `starting` event occurs when the game first loads. It cannot take any parameters,
and it must produce the game state of the world. Typically, this will be a dictionary.

.. _starting_handler:

.. py:function:: starting_handler()

    :return: The new state of the world.

    The starting event.

`updating`
==========

The `updating` event is by far the most common.

.. py:function:: updating_handler(world)
                 updating_handler(world, delta)

    :param world: The current state of the world. Initially, the value that you returned from your :ref:`starting_handler<starting_handler>`.
    :param delta: Optional parameter representing the number of seconds that has passed since the last frame. Typically only necessary in high-performance games.
    :type delta: float

    Binds a function to the

    .. code-block:: python

        def update_the_world(world):
            pass

        when('updating', update_the_world)

Others
======

`typing`

`clicking`

Custom event test
=================