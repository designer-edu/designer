import pygame
import math

from designer.colors import _process_color
from designer.helpers import get_width, get_height
from designer.objects.designer_object import DesignerObject
from designer.core.internal_image import InternalImage, DesignerSurface
from designer.utilities.vector import Vec2D
from designer.utilities.util import _anchor_offset


class Rectangle(DesignerObject):
    FIELDS = (*DesignerObject.FIELDS, 'color', 'border')

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

        self._pos = center
        self._anchor = anchor
        # Rectangle specific data
        self._size = Vec2D(width, height)
        self._color = color
        self._border = border

        # And draw!
        self._redraw_internal_image()

    def __repr__(self):
        return f"<rectangle({self._color!r}, {self._size[0]}, {self._size[1]})>"

    def _recalculate_offset(self):
        size = self._size * self._scale
        offset = _anchor_offset(self._anchor, size[0], size[1])
        self._offset = Vec2D(offset) - self._transform_offset

    def _redraw_internal_image(self):
        # No flipping
        # Scaling
        width = self._size[0] * self._scale[0]
        height = self._size[1] * self._scale[1]
        size = (int(width), int(height))
        color = _process_color(self._color)
        if size[0] <= 0 or size[1] <= 0:
            target = InternalImage(size=(1, 1)).fill(color)
            self._transform_image = target._surf
            self._recalculate_offset()
            self._expire_static()
            return
        new_image = InternalImage(size=size)
        new_image.draw_rect(color, (0, 0), size, self._border or 0)
        # Rotation
        if self._angle != 0:
            old = Vec2D(new_image.rect.center)
            new_image.rotate(self._angle % 360)
            new = new_image.rect.center
            self._transform_offset = old - new
        self._transform_image = new_image._surf
        self._recalculate_offset()
        self._expire_static()

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


def rectangle(color, width, height=None, x=None, y=None, anchor='center', border=None):
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
    return Rectangle((x, y), anchor, width, height, color, border)