Designer Documentation for Students
===================================

Designer Objects and Grouping Objects
-------------------------------------

.. automodule:: designer.DesignerObject

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

.. function:: rectangle(color, left, top, width, height)

    Function to create a rectangle.

    :param color: color of rectangle
    :type color: str
    :param left: left most x-coordinate of rectangle
    :type left: int
    :param top: top most y-coordinate of rectangle
    :type top: int
    :param width: width of ellipse in rectangle
    :type width: int
    :param height: height of ellipse in rectangle
    :type height: int
    :return: Rectangle object created

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
    :param start_angle: angle to start drawing arc at
    :type start_angle: int
    :param stop_angle: angle to stop drawing arc at
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

.. automodule:: designer.Animation
   :members: glide_around, glide_down, glide_in_degrees, glide_left, glide_right, glide_up, rotate


Settings
--------
.. automodule:: designer.Director
    :members: draw, set_window_color, set_window_size, get_width, get_height
