import pygame

import math

from designer.colors import _process_color
from designer.helpers import get_width, get_height
from designer.objects.designer_object import DesignerObject
from designer.core.internal_image import InternalImage, DesignerSurface
from designer.utilities.vector import Vec2D
from designer.utilities.util import _anchor_offset


class Line(DesignerObject):
    FIELDS = (*DesignerObject.FIELDS,
              'start_x', 'start_y', 'end_x', 'end_y',
              'start', 'end', 'thickness', 'color')


    def __init__(self, start, end, thickness, color):
        """
        Creates Line Designer Object on window.

        :param start: starting coordinates of line
        :type start: Tuple[int]
        :param end: ending coordinates of line
        :type end: Tuple[int]
        :param thickness: thickness of line in pixels
        :type thickness: int
        :param color: color of line
        :type color: str or List[str]
        """
        super().__init__()
        self._color = color
        self._thickness = thickness
        self._calculate_positions(start, end, thickness)

        # And draw!
        self._redraw_internal_image()

    def _calculate_positions(self, start, end, thickness):
        (x1, y1), (x2, y2) = start, end
        # Need to flip y-axis
        angle = math.atan2(-(y2 - y1), x2 - x1) % 2 * math.pi
        p1x, p1y = x1 + math.cos(angle + math.pi / 2) * thickness, y1 + math.sin(angle + math.pi / 2) * thickness
        p2x, p2y = x1 + math.cos(angle - math.pi / 2) * thickness, y1 - math.sin(angle + math.pi / 2) * thickness
        p3x, p3y = x2 + math.cos(angle + math.pi / 2) * thickness, y2 + math.sin(angle + math.pi / 2) * thickness
        p4x, p4y = x2 + math.cos(angle - math.pi / 2) * thickness, y2 - math.sin(angle + math.pi / 2) * thickness
        left = min(p1x, p2x, p3x, p4x)
        right = max(p1x, p2x, p3x, p4x)
        top = min(p1y, p2y, p3y, p4y)
        bottom = max(p1y, p2y, p3y, p4y)

        # calculate differences between x and y coordinates of line
        x = abs(start[0] - end[0])
        y = abs(start[1] - end[1])

        width = right - left
        height = bottom - top

        new_start = (x1 - left), (y1 - top)
        new_end = (x2 - left), (y2 - top)

        self._pos = (left, top)
        self._start = new_start
        self._end = new_end
        self._size = (width, height)

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
        new_image.draw_lines(color, [self._start, self._end], self._thickness, False)
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
    def start_x(self):
        return self._start[0]

    @start_x.setter
    def start_x(self, value):
        self._start = (self._start[0], value)
        self._calculate_positions(self._start, self._end, self._thickness)
        self._redraw_internal_image()

    @property
    def start_y(self):
        return self._start[1]

    @start_y.setter
    def start_y(self, value):
        self._start = (value, self._start[1])
        self._calculate_positions(self._start, self._end, self._thickness)
        self._redraw_internal_image()

    @property
    def end_x(self):
        return self._end[0]

    @end_x.setter
    def end_x(self, value):
        self._end = (self._end[0], value)
        self._calculate_positions(self._start, self._end, self._thickness)
        self._redraw_internal_image()

    @property
    def end_y(self):
        return self._end[1]

    @end_y.setter
    def end_y(self, value):
        self._end = (value, self._end[1])
        self._calculate_positions(self._start, self._end, self._thickness)
        self._redraw_internal_image()

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = value
        self._redraw_internal_image()

    @property
    def thickness(self):
        return self._thickness

    @thickness.setter
    def thickness(self, value):
        self._thickness = value
        self._redraw_internal_image()

def line(color, start_x, start_y, end_x=None, end_y=None, thickness=1):
    '''
    Function to create a line.

    :param thickness: thickness of line in pixels
    :type thickness: int
    :param color: color of line
    :type color: str or List[str]
    :param args: start and end coordinates of line
    :type args: two tuples (start x, start y), (end x, end y) or four ints start x, start y, end x, end y

    :return: Line object created
    '''
    if end_x is None and end_y is None:
        end_x, end_y = start_y
        start_x, start_y = start_x
    return Line((start_x, start_y), (end_x, end_y), thickness, color)