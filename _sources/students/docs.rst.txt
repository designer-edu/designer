.. _fulldocs:

Designer Documentation for Students
===================================

Creating DesignerObjects
------------------------

.. _image:

.. function:: image(path)
              image(path, x, y)

    Function to create an image from the given `path`. The `path` given
    can be a local file or a URL to a remote image. Keep in mind that
    loading large URLs can take a little while.

    .. code-block:: python

        from designer import *
        # A random corgi picture from a website
        image("http://placecorgi.com/260/180")

    We recommend always storing images as local files in adjacent folders,
    to simplify problems with paths. Never use absolute file locations like
    `C:/Users/acbart...` or `/usr/acbart/`, but instead use relative paths.

    Most popular image formats are supported: `png`, `gif`, `bmp`, `jpeg`.

    Animated gifs are partially supported, although many suffer from corruption.

    :param path: local file path or url of image to use
    :type path: str
    :param x: horizontal location to draw the image
    :type x: int
    :param y: vertical location to draw the image
    :type y: int
    :return: Image object created
    :rtype: DesignerObject

.. _emoji:

.. function:: emoji(name)
              emoji(name, x, y)

    Function to create an emoji of the given `name`. You can also provide the actual unicode character.
    Not every unicode emoji is supported. You can find a `searchable emoji list here <https://emojis.wiki/>`_. Copy
    paste the emoji as a string literal as the `name` argument.

    .. code-block:: python

        from designer import *
        # Either of these will create a picture of a dog on your screen
        emoji("dog")
        emoji("🐕")

    :param name: The unicode name of the emoji, or the unicode character of the emoji.
    :type name: str
    :param x: horizontal location to draw the emoji
    :type x: int
    :param y: vertical location to draw the emoji
    :type y: int
    :return: Emoji image object created
    :rtype: DesignerObject


.. _text:

.. function:: text(color, text)
              text(color, text, size)
              text(color, text, size, x, y)
              text(color, text, size, x, y, font_name='Arial')

    Function to create text on the screen with the given color.
    Not all unicode characters are supported!

    .. code-block:: python

        from designer import *
        # Black text that reads "Hello world!"
        text("black", "Hello world!")

    :param color: The :ref:`color<color>` of the text
    :type color: str
    :param message: text to appear on window
    :type message: str
    :param size: Font size of the text
    :type size: int
    :param x: left most x-coordinate of text
    :type x: int
    :param y: top most y-coordinate of text
    :type y: int
    :param font_name: The name of the font to use. Defaults to 'Arial'.
    :type font_name: str
    :return: Text object created
    :rtype: DesignerObject

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

.. _circle:

.. function:: circle(color, radius)
              circle(color, radius, x, y)
              circle(color, radius, x, y, border=None, anchor='center')

    Function to create a circle with the given `radius`. Defaults to
    being drawn at the center of the screen, from the center of the
    circle.

    .. code-block:: python

        from designer import *
        # Black circle of radius 100
        circle("black", 100)

        # Red circle of radius 50 in topleft corner
        # Part of the circle will be caught off since its drawn from the center
        red_circle = circle("red", 50, 0, 0)

        # Once created, you can manipulate the border and other properties
        red_circle['color'] = 'purple'
        red_circle['x'] = 100

    You can also control the border of the circle in order to make the shape not be
    filled, but instead just a bordered circle.

    .. code-block:: python

        # Blue circle of size 75, not filled
        empty = circle("blue", 75, border=1)
        empty['border'] = 7

    And like any other shape, you can specify an :ref:`anchor<anchor>` to adjust the "pin" of the
    object relative to its position.

    .. code-block:: python

        # Blue 50-radius circle drawn from the topleft corner, at position 0,0
        circle("blue", 50, 0, 0, anchor='topleft')

    :param color: The :ref:`color<color>` of the circle
    :type color: str
    :param radius: radius of circle in pixels
    :type radius: int
    :param x: The horizontal position in the Window. If not specified, defaults to the center of the window.
    :type x: int
    :param y: The vertical position in the Window. If not specified, defaults to the center of the window.
    :type y: int
    :param border: If given, the circle is not filled; instead, the center of the circle is empty and only a border is shown. The thickness of the border is given by this value.
    :type border: int
    :param anchor: An :ref:`anchor<anchor>` indicating where the "pin" (or "center") of the object should be relative to its position.
    :type anchor: str
    :return: Circle object created
    :rtype: DesignerObject

.. _ellipse:

.. py:function:: ellipse(color, width, height)
                 ellipse(color, width, height, x, y)
                 ellipse(color, width, height, x, y, border=None, anchor='center')

    Function to create an ellipse object. You must specify the color, width, and height
    of the ellipse. Optionally, you can also position it at a specific x/y coordinate,
    although it will default to the center of the Window.

    .. code-block:: python

        from designer import *
        # Black ellipse of size 100x100
        ellipse("black", 100, 100)

        # Red ellipse of size 50x50 in topleft corner
        # Part of the rectangle will be caught off since its drawn from the center
        red_ellipse = ellipse("red", 50, 50, 0, 0)

        # Once created, you can manipulate the border and other properties
        red_ellipse['color'] = 'purple'
        red_ellipse['x'] = 100

    You can also control the border of the ellipse in order to make the shape not be
    filled, but instead just a bordered ellipse.

    .. code-block:: python

        # Blue ellipse of size 75x100, not filled
        empty = ellipse("blue", 75, 100, border=1)
        empty['border'] = 7

    And like any other shape, you can specify an :ref:`anchor<anchor>` to adjust the "pin" of the
    object relative to its position.

    .. code-block:: python

        # Blue 50x50 ellipse drawn from the topleft corner, at position 0,0
        ellipse("blue", 50, 50, 0, 0, anchor='topleft')

    :param color: The :ref:`color<color>` of the ellipse
    :type color: str
    :param width: The horizontal width of the ellipse
    :type width: int
    :param height: The vertical height of the ellipse
    :type height: int
    :param x: The horizontal position in the Window. If not specified, defaults to the center of the window.
    :type x: int
    :param y: The vertical position in the Window. If not specified, defaults to the center of the window.
    :type y: int
    :param border: If given, the ellipse is not filled; instead, the center of the ellipse is empty and only a border is shown. The thickness of the border is given by this value.
    :type border: int
    :param anchor: An :ref:`anchor<anchor>` indicating where the "pin" (or "center") of the object should be relative to its position.
    :type anchor: str

    :return: Ellipse designer object created
    :rtype: DesignerObject

.. _line:

.. function:: line(color, start_x, start_y, end_x, end_y)
              line(color, start_x, start_y, end_x, end_y, thickness=1)

    Function to create a line, beginning at the coordinates given by
    `(start_x, start_y)` and ending at the coordinates given by
    `(end_x, end_y)`. These coordinates are given as absolute values,
    and must be provided.

    .. code-block:: python

        # Blue line stretching from 0,0, to 50, 100
        line("blue", 0, 0, 50, 100)

    .. code-block:: python

        # Thick Red line stretching from the middle to the bottom right
        line("red", 400, 300, 800, 600, thickness=6)

    :param color: The :ref:`color<color>` of the line
    :type color: str
    :param start_x: x-coordinate at which to start line
    :type start_x: int
    :param start_y: y-coordinate at which to start line
    :type start_y: int
    :param end_x: x-coordinate at which to end line
    :type end_x: int
    :param end_y: y-coordinate at which to end line
    :type end_y: int
    :param thickness: thickness of line in pixels
    :type thickness: int
    :return: Line designer object created
    :rtype: DesignerObject

.. _arc:

.. function:: arc(color, start_angle, stop_angle, width, height)
              arc(color, start_angle, stop_angle, width, height, x, y)
              arc(color, start_angle, stop_angle, width, height, x, y, thickness=1, anchor='center')

    Function to make an arc, as if it were part of an ellipse. Think of the
    arc as being part of the border of an ellipse with the given width/height;
    then the `start_angle` and `stop_angle` are the slice (in degrees) of the
    border that will actually be drawn. This is a line, not a polygon, so there
    is no option to fill in the arc.

    .. code-block:: python

        from designer import *
        # Black arc of size 100x100, from 0 to 90 degrees (quarter circle)
        arc("black", 0, 90, 100, 100)
        # Black arc of size 100x100, from 135 to 270 degrees (2/3 circle)
        arc("black", 135, 270, 100, 100)

        # Red U of size 50x50 in topleft corner
        # Part will be cut off unless you change the anchor!
        red_U = arc("red", 180, 360, 50, 50, 0, 0)

        # Once created, you can manipulate the thickness and other properties
        red_U['anchor'] = 'topleft'
        red_U['thickness'] = 10

    :param color: The :ref:`color<color>` of the arc
    :type color: str
    :param start_angle: angle in degrees to start drawing arc at
    :type start_angle: int
    :param stop_angle: angle in degrees to stop drawing arc at
    :type stop_angle: int
    :param width: The horizontal width of the arc, as if it were a complete ellipse
    :type width: int
    :param height: The vertical height of the arc, as if it were a complete ellipse
    :type height: int
    :param x: left most x-coordinate of arc
    :type x: int
    :param y: top most y-coordinate of arc
    :type y: int
    :param thickness: thickness of arc in pixels
    :type thickness: int
    :return: Arc object created
    :rtype: DesignerObject

.. _shape:

.. function:: shape(color, x1, y1, x2, y2, x3, y3, ...)
              shape(color, points)

    Function to create a shape of at least three points. The points should be relative to each other.
    The resulting image will be centered in the middle of the window, which can be adjusted by using `x` and `y`.
    If you want to absolutely position the image instead, then use `lines`.

    :param color: color of shape.
    :type color: str
    :param points: coordinates of points of shape
    :type points: List[Tuple] in (x, y), (x, y) format of points to be connected of shape
    :return: Shape object created

.. _lines:

.. function:: lines(color, x1, y1, x2, y2, x3, y3, ...)
              lines(color, points)

    Function to create a shape of at least three points. The points will be absolutely positioned in the window.

    :param color: color of shape.
    :type color: str
    :param points: coordinates of points of shape
    :type points: List[Tuple] in (x, y), (x, y) format of points to be connected of shape
    :return: Shape object created

.. _group:

.. function:: group(object1, ...)
              group(objects)

    Function to group any number of Designer `objects` together. They will produce one single picture when they are done.
    The advantage of grouping together a bunch of objects is that they become easier to rotate and scale together.

    :param objects: collection of objects to be grouped together for collective functionality
    :type objects: at least one DesignerObject
    :return: Created Designer Group object


Designer Objects Attributes
---------------------------

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

.. py:attribute:: width
    :type: integer

    The horizontal size of the object on the screen.

    .. code-block:: python

        box = rectangle('red', 50, 50)
        # Set to be 100 pixels wide
        box['width'] = 100
        # Increase width by 10 pixels
        box['width'] += 10

.. py:attribute:: height
    :type: integer

    The vertical size of the object on the screen.

    .. code-block:: python

        box = rectangle('red', 50, 50)
        # Set to be 100 pixels tall
        box['height'] = 100
        # Increase height by 10 pixels
        box['height'] += 10

.. py:attribute:: scale_x
    :type: float

    How much to multiply the object's width by in calculating its final horizontal
    size on the screen.

    .. code-block:: python

        box = rectangle('red', 50, 50)
        # Will be drawn twice as wide
        box['scale_x'] = 2.0
        # Will be drawn half as wide
        box['scale_x'] = .5

.. py:attribute:: scale_y
    :type: float

    How much to multiply the object's height by in calculating its final vertical
    size on the screen.

    .. code-block:: python

        box = rectangle('red', 50, 50)
        # Will be drawn twice as tall
        box['scale_y'] = 2.0
        # Will be drawn half as tall
        box['scale_y'] = .5

.. py:attribute:: angle
    :type: float

    An amount to rotate the image, in degrees (0-360). You can provide negative
    values and amounts greater than 360.

    .. code-block:: python

        box = rectangle('red', 50, 50)
        # Will be drawn at a 45 degree angle
        box['angle'] = 45
        # Rotates it 180 degrees around
        box['angle'] += 180

.. py:attribute:: flip_x
    :type: boolean

    Whether or not to horizontally mirror this shape to the other direction.
    Note that symmetric shapes have no effect when they are mirrored, even
    if they are rotated. The order of transformations is flipping, scaling,
    and then rotating.

    .. code-block:: python

        ada = image('ada.png', 50, 50)
        # Will be flipped horizontally
        ada['flip_x'] = True
        # Will not be flipped horizontally
        ada['flip_x'] = False

.. py:attribute:: flip_y
    :type: boolean

    Whether or not to vertically mirror this shape to the other direction.
    Note that symmetric shapes have no effect when they are mirrored, even
    if they are rotated. The order of transformations is flipping, scaling,
    and then rotating.

    .. code-block:: python

        ada = image('ada.png', 50, 50)
        # Will be flipped vertically
        ada['flip_y'] = True
        # Will not be flipped vertically
        ada['flip_y'] = False

.. py:attribute:: visible
    :type: boolean

    Whether or not this object should actually be drawn on screen, or whether
    it will be hidden. Objects that are invisible still get "update" events.

    .. code-block:: python

        box = rectangle('red', 50, 50)
        # Will not be drawn
        ada['visible'] = False
        # Will be drawn
        ada['visible'] = True

.. py:attribute:: alpha
    :type: float

    A value from 0..1 indicating the amount of transparency (or "opacity") that
    this object should have when it is being drawn on the screen.

    .. code-block:: python

        box = rectangle('red', 50, 50)
        # Partially transparent
        ada['alpha'] = .5
        # Fully invisible
        ada['alpha'] = 0.0
        # Fully visible
        ada['alpha'] = 1.0

.. py:attribute:: scale
    :type: [scale_x, scale_y]

    The combined horizontal and vertical scale of the object on the screen,
    as a list of two values. You can also set a single value in order to control
    both properties at the same time.


.. py:attribute:: size
    :type: [width, height]

    The combined width and height of the object on the screen, as a list of two values.

.. py:attribute:: pos
    :type: [x, y]

    The position of the object on the screen, as a list of two values.


Designer Object Functions
-------------------------

.. _move_forward:

.. py:function:: move_forward(object, amount)
                 move_forward(object, amount, angle)

    Move the given `object` forward by `amount`, either in its current rotation
    `angle` attribute or the given `angle`. This changes the `x` and `y` attribute
    of the Designer Object, in addition to returning the value.

    .. code-block:: python

        from designer import *
        # Black rectangle of size 100x100
        # Defaults to angle=0 (pointing to the right)
        box = rectangle("black", 100, 100)

        # Move the box to the right 50 pixels
        move_forward(box, 50)

        # Move the box upwards 20 pixels
        move_forward(box, 20, 90)

        # Move the box down and left, both 10 pixels, by chaining
        move_forward(move_forward(box, 10, 270), 10, 180)

    :param object: A Designer Object
    :type object: DesignerObject
    :param amount: The number of pixels to move
    :type amount: int
    :param angle: The direction (in degrees) to move in; defaults to the object's current `angle` attribute (which defaults to 0).
    :type angle: int

    :return: The Designer Object that was passed in.
    :rtype: DesignerObject

Animation
---------

.. automodule:: designer.animation
   :members: glide_down, glide_in_degrees, glide_left, glide_right, glide_up, spin


Settings
--------

.. _get_width:

.. py:function:: get_width()

    Returns the horizontal size of the Window.

    :rtype: int

.. _get_height:

.. py:function:: get_height()

    Returns the vertical size of the Window.

    :rtype: int

.. _set_window_title:

.. py:function:: set_window_height(message)
                 set_window_height(None)

    Changes the caption displayed at the top of the window. If you set the message to
    be `None` instead, then it will render internal debug information about the
    number of static and non-static objects being drawn on the screen.

    :param message: The text to render in the screen.
    :param type: str


.. py:function:: set_window_color(color)

    Changes the background color of the window to whatever :ref:`color<color>` you specify.
    Defaults to `'white'`.

    .. code-block:: python

        from designer import *
        # Black text that reads "Hello world!"
        set_window_color('blue')

    :param color: The :ref:`color<color>` to set the background to.
    :param type: str

Events
------

.. _when:

.. py:function:: when(event_name, event_handler)
                 when(predicate_function, event_handler)
                 when('starting', event_handler)
                 when('updating', event_handler)
                 when('typing', event_handler)
                 when('clicking', event_handler)

    Binds the function given by `event_handler` to the `event_name`.

Collisions
----------

.. _colliding:

.. py:function:: colliding(object, x, y) -> bool
                 colliding(object, other_object) -> bool

    Tests if the object is colliding with either the point or the other object.

    :param object: A DesignerObject
    :type object: DesignerObject
    :param x: The horizontal position to check.
    :type x: int
    :param y: The vertical position to check.
    :type y: int
    :param other_object: Another DesignerObject to check against.
    :type other_object: DesignerObject
    :rtype: bool

Game Control
------------

.. _stop:

.. py:function:: stop()

    Stops the game completely, closing the window.

.. _pause:

.. py:function:: pause()

    Pauses the game, keeping the window open and whatever the last thing to draw was.
    However, no further events will be processed (besides the `'quitting'` event).
