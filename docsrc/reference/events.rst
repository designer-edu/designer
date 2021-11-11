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

The `updating` event is by far the most common. It happens every step of the world.

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

'clicking'
==========

The `clicking` event is when the mouse is clicked down.

.. py:function:: clicking_handler(world, x, y)
                 clicking_handler(world, x, y, button)

    :param world: The current state of the world. Initially, the value that you returned from your :ref:`starting_handler<starting_handler>`.
    :param x: The current horizontal position of the mouse.
    :type x: int
    :param y: The current vertical position of the mouse.
    :type y: int
    :param button: The mouse button that was clicked. One of either `'left'`, `'middle'`, or `'right'`.
    :type button: str

    Binds a function to the mouse being clicked.

    .. code-block:: python

        def handle_mouse_click(world, x, y, button):
            pass

        when('clicking', handle_mouse_click)

'typing'
========

The `typing` event happens when you press a key on the keyboard.

.. py:function:: typing_handler(world, key)
                 typing_handler(world, key, character)

    :param world: The current state of the world. Initially, the value that you returned from your :ref:`starting_handler<starting_handler>`.
    :param key: A user-friendly name for whatever key was pressed, such as `'left'` (for the left arrow) or `'space'`. A semi-complete list can be found at :ref:`keys<keys>`.
    :type key: str
    :param character: A string representation of the keyboard character, representing what the character looks like when typed. The `space` key would be represented as a `' '` here.
    :type character: str

    Binds a function to the `'typing'` handler.

    .. code-block:: python

        def handle_the_keyboard(world):
            pass

        when('typing', handle_the_keyboard)

All Possible Events
===================

This is a list of all the events that are possible:

* `'input.mouse.down'`
* `'input.mouse.up'`
* `'input.keyboard.down'`

Custom event test
=================