import pygame

import math

from designer.colors import _process_color
from designer.helpers import get_width, get_height
from designer.objects.designer_object import DesignerObject
from designer.core.internal_image import InternalImage, DesignerSurface
from designer.utilities.vector import Vec2D
from designer.utilities.util import _anchor_offset


class Arc(DesignerObject):
    DEFAULT_BORDER_WIDTH = 1
    FIELDS = (*DesignerObject.FIELDS, 'color', 'border')

    def __init__(self, center, width, height, start_angle, stop_angle, anchor, color, border, **kwargs):
        """
        Creates an Arc Designer Object on window.

        :param color: color to draw arc
        :type color: str or List[str]
        :param start_angle: angle to start drawing arc at
        :type start_angle: int
        :param stop_angle: angle to stop drawing arc at
        :type stop_angle: int
        :param thickness: thickness of arc in pixels
        :type thickness: int
        :param left: x coordinate of top left corner of arc
        :type left: int
        :param top: y coordinate of top left corner of arc
        :type top: int
        :param width: width of arc to be drawn
        :type width: int
        :param height: height of arc to be drawn
        :type height: int
        """
        super().__init__(**kwargs)

        x, y = center
        x = x if x is not None else get_width() / 2
        y = y if y is not None else get_height() / 2
        center = x, y

        self._pos = center
        self._anchor = anchor
        # Ellipse specific data
        self._size = Vec2D(width, height)
        self._start_angle = start_angle
        self._stop_angle = stop_angle
        self._color = color
        self._border = border

        # And draw!
        self._redraw_internal_image()

    def _recalculate_offset(self):
        size = self._size * self._scale
        offset = _anchor_offset(self._anchor, size[0], size[1])
        self._offset = Vec2D(offset) - self._transform_offset

    def _redraw_internal_image(self):
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
        new_image.draw_arc(color,
                           math.pi/180 * self._start_angle,
                           math.pi/180 * self._stop_angle,
                           (0, 0), self._size, self._border)
        # Flip
        if self._flip_x or self._flip_y:
            new_image.flip(self._flip_x, self._flip_y)
        # Rotation
        if self._angle != 0:
            angle = self._angle % 360
            old = Vec2D(new_image.rect.center)
            new_image.rotate(angle)
            new = new_image.rect.center
            self._transform_offset = old - new
        self._transform_image = new_image._surf
        self._recalculate_offset()
        self._expire_static()

    @property
    def start_angle(self):
        return self._start_angle

    @start_angle.setter
    def start_angle(self, value):
        self._start_angle = value
        self._redraw_internal_image()

    @property
    def stop_angle(self):
        return self._stop_angle

    @stop_angle.setter
    def stop_angle(self, value):
        self._stop_angle = value
        self._redraw_internal_image()

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


def arc(color, start_angle, stop_angle, width, height,
        x=None, y=None, thickness=1, anchor='center', **kwargs):
    """
    Function to make an arc.

    :param color: color to draw arc
    :type color: str or List[str]
    :param start_angle: angle to start drawing arc at
    :type start_angle: int
    :param stop_angle: angle to stop drawing arc at
    :type stop_angle: int
    :param thickness: thickness of arc in pixels
    :type thickness: int
    :param args: left top corner of arc and width and height of arc
    :type args: two Tuples (left, top), (width, height) or four ints left, top, width, height
    :return: Arc object created
    """
    return Arc((x, y), width, height, start_angle, stop_angle, anchor, color, thickness, **kwargs)