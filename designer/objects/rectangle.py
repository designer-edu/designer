import pygame
import math

from designer.colors import _process_color
from designer.helpers import get_width, get_height
from designer.objects.designer_object import DesignerObject
from designer.core.internal_image import InternalImage
from designer.utilities.vector import Vec2D
from designer.utilities.surfaces import DesignerSurface


class Rectangle(DesignerObject):
    DEFAULT_BORDER_WIDTH = 1

    def __init__(self, center, anchor, width, height, color, border):
        """
        Creates Rectangle Designer Object on window.

        :param center: x, y coordinates of center of circle
        :type center: Tuple[int]
        :param anchor: the anchor to draw the circle at
        :type anchor: str
        :param width: width of rectangle in pixels
        :type width: int
        :param height: height of rectangle in pixels
        :type height: int
        :param color: color of rectangle
        :type color: str or List[str]
        :param border: the width of the circle's line (0 is used for a filled circle)
        :type border: int
        """
        super().__init__()

        x, y = center
        x = x if x is not None else get_width() / 2
        y = y if y is not None else get_height() / 2
        center = x, y

        self.pos = center
        self.anchor = anchor
        # Rectangle specific data
        self._width = width
        self._height = height
        self._color = color
        self._border = border

        # Draw the actual rectangle image
        self._internal_image = self._redraw_internal_image()
        self._transform_image = self._internal_image._surf

    def _redraw_internal_image(self):
        if int(self._width) > 0 and int(self._height) > 0:
            new_image = InternalImage(size=(self._width, self._height))
            new_image.draw_rect(_process_color(self._color),
                                (0, 0),
                                (self._width, self._height),
                                self._border)
            return new_image
        else:
            return InternalImage(size=(1, 1))

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = value
        self._redraw_internal_image()

    @property
    def border(self):
        return self._border

    @border.setter
    def border(self, value):
        self._border = value
        self._redraw_internal_image()


def rectangle(color, width, height=None, x=None, y=None,
              anchor='center', border=None, filled=True):
    '''
    Function to create a rectangle.

    :param color: color of rectangle
    :type color: str or List[str]
    :param args: left top corner of image and width and height of rectangle
    :type args: two Tuples (left, top), (width, height) or four ints left, top, width, height
    :return: Rectangle object created
    '''
    if x is not None and y is None:
        x, y = x
    elif x is None and y is None and height is not None:
        if not isinstance(height, (int, float)):
            x, y = height
            width, height = width
    elif height is None:
        width, height = width
    if filled is True:
        border = 0
    elif filled is False:
        border = border or Rectangle.DEFAULT_BORDER_WIDTH
    elif border is None:
        border = Rectangle.DEFAULT_BORDER_WIDTH
    return Rectangle((x, y), anchor, width, height, color, border)