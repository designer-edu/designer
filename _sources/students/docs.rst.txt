Designer Documentation for Students
===================================

Designer Objects
----------------

.. automodule:: designer.DesignerObject

.. py:attribute:: x
    :type: integer

    The horizontal position of the object on the screen.

    .. code-block:: python

        box = rectangle('red', 50, 50)
        # Set to be 100 pixels from the left-hand side of the window
        box['x'] = 100
        # Move 5 pixels left
        box['x'] -= 5

.. py:attribute:: y
    :type: integer

    The vertical position of the object on the screen.

    .. code-block:: python

        box = rectangle('red', 50, 50)
        # Set to be 100 pixels from the top of the window
        box['y'] = 100
        # Move 5 pixels up
        box['y'] -= 5

.. py:attribute:: pos
    :type: [x, y]

    The position of the object on the screen.

Specific DesignerObjects
########################

.. _rectangle:

.. py:function:: rectangle(color, width, height)
                 rectangle(color, width, height, x, y)
                 rectangle(color, width, height, x, y, border=None, anchor='center')

    Function to create a rectangle object. You must specify the color, width, and height
    of the rectangle. Optionally, you can also position it at a specific x/y coordinate,
    although it will default to the center of the Window.

    .. code-block:: python

        from designer import *
        # Black rectangle of size 100x100
        rectangle("black", 100, 100)

        # Red rectangle of size 50x50 in topleft corner
        # Part of the rectangle will be caught off since its drawn from the center
        red_box = rectangle("red", 50, 50, 0, 0)

        # Once created, you can manipulate the border and other properties
        red_box['color'] = 'purple'
        red_box['x'] = 100

    You can also control the border of the rectangle in order to make the shape not be
    filled, but instead just a bordered rectangle.

    .. code-block:: python

        # Blue rectangle of size 75x100, not filled
        empty = rectangle("blue", 75, 100, border=1)
        empty['border'] = 7

    And like any other shape, you can specify an :ref:`anchor<anchor>` to adjust the "pin" of the
    object relative to its position.

    .. code-block:: python

        # Blue 50x50 rectangle drawn from the topleft corner, at position 0,0
        rectangle("blue", 50, 50, 0, 0, anchor='topleft')

    :param color: The :ref:`color<color>` of the rectangle
    :type color: str
    :param width: The horizontal width of the rectangle
    :type width: int
    :param height: The vertical height of the rectangle
    :type height: int
    :param x: The horizontal position in the Window. If not specified, defaults to the center of the window.
    :type x: int
    :param y: The vertical position in the Window. If not specified, defaults to the center of the window.
    :type y: int
    :param border: If given, the rectangle is not filled; instead, the center of the rectangle is empty and only a border is shown. The thickness of the border is given by this value.
    :type border: int
    :param anchor: An :ref:`anchor<anchor>` indicating where the "pin" (or "center") of the object should be relative to its position.
    :type anchor: str

    :return: Rectangle designer object created
    :rtype: DesignerObject

.. function:: line(color, thickness, start_x, start_y, end_x, end_y)

    Function to create a line.

    :param color: color of line
    :type color: str
    :param thickness: thickness of line in pixels
    :type thickness: int
    :param start_x: x-coordinate at which to start line
    :type start_x: int
    :param start_y: y-coordinate at which to start line
    :type start_y: int
    :param end_x: x-coordinate at which to end line
    :type end_x: int
    :param end_y: y-coordinate at which to end line
    :type end_y: int
    :return: Line object created

.. function:: circle(color, radius, center_x, center_y)

    Function to create a circle.

    :param color: color of circle
    :type color: str
    :param radius: radius of circle in pixels
    :type radius: int
    :param center_x: x-coordinate of center of circle
    :type center_x: int
    :param center_y: y-coordinate of center of circle
    :type center_y: int
    :return: Circle object created

.. function:: ellipse(color, left, top, width, height)

    Function to make an ellipse.

    :param color: color of ellipse
    :type color: str or List[str]
    :param left: left most x-coordinate of ellipse
    :type left: int
    :param top: top most y-coordinate of ellipse
    :type top: int
    :param width: width of ellipse in pixels
    :type width: int
    :param height: height of ellipse in pixels
    :type height: int
    :return: Ellipse object created

.. function:: arc(color, start_angle, stop_angle, thickness, left, top, width, height)

    Function to make an arc.

    :param color: color to draw arc
    :type color: str
    :param start_angle: angle in radians to start drawing arc at
    :type start_angle: int
    :param stop_angle: angle in radians to stop drawing arc at
    :type stop_angle: int
    :param thickness: thickness of arc in pixels
    :type thickness: int
    :param left: left most x-coordinate of arc
    :type left: int
    :param top: top most y-coordinate of arc
    :type top: int
    :param width: width of arc in pixels
    :type width: int
    :param height: height of arc in pixels
    :type height: int
    :return: Arc object created

.. function:: text(text_color, text, text_size, left, top)

    Function to create text.

    :param color: color of text
    :type color: str or List[str]
    :param text: text to appear on window
    :type text: str
    :param left: left most x-coordinate of text
    :type left: int
    :param top: top most y-coordinate of text
    :type top: int
    :return: Text object created

.. function:: image(path, left, top, width, height)

    Function to create an image.

    :param path: local file path or url of image to upload
    :type path: str
    :param left: left most x-coordinate of image
    :type left: int
    :param top: top most y-coordinate of image
    :type top: int
    :param width: width of image in pixels
    :type width: int
    :param height: height of image in pixels
    :type height: int
    :return: Image object created

.. function:: shape(color, points)

    Function to create a shape of at least three points.

    :param color: color of shape.
    :type color: str
    :param points: coordinates of points of shape
    :type points: List[Tuple] in (x, y), (x, y) format of points to be connected of shape
    :return: Shape object created

.. function:: group(*objects)

    Function to group multiple objects together.

    :param objects: collection of objects to be grouped together for collective functionality
    :type objects: at least one DesignerObject
    :return: Created Designer Group object

Animation
---------

.. automodule:: designer.animation
   :members: glide_down, glide_in_degrees, glide_left, glide_right, glide_up, spin


Settings
--------
.. automodule:: designer.helpers
    :members: draw, set_window_color, set_window_size, get_width, get_height

Events
------

.. _when:

.. py:function:: when(event_name, event_handler)
                 when(predicate_function, event_handler)

    Binds the function given by `event_handler` to the `event_name`.
