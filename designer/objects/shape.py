import math
from typing import List

import pygame

import designer
from designer.core.internal_image import DesignerSurface, InternalImage
from designer.colors import _process_color
from designer.helpers import get_width, get_height
from designer.objects.designer_object import DesignerObject
from designer.utilities.vector import Vec2D
from designer.utilities.util import rect_from_points, _anchor_offset
from designer.utilities.argument_checks import is_non_empty_iterable_of_points, at_least_three, are_numbers


class Shape(DesignerObject):
    DEFAULT_BORDER_WIDTH = 1
    FIELDS = (*DesignerObject.FIELDS, 'points', 'color', 'border')

    def __init__(self, center, points, anchor, color, border, absolute):

        super().__init__()

        x = center[0] if center[0] is not None else get_width()/2
        y = center[1] if center[1] is not None else get_height()/2

        self._pos = Vec2D(x, y)
        self._anchor = anchor
        # Polygon specific data
        self._border = border
        self._points: List[Vec2D] = [Vec2D(p) for p in points]
        self._bounds = self._get_bounds()
        self._size = self._bounds.size
        self._color = color

        if absolute:
            self._pos = self._bounds.topleft

        # And Draw!
        self._redraw_internal_image()

    def _get_bounds(self):
        if not self._points:
            return Vec2D(1, 1)
        bounds = rect_from_points(self._points)
        print(bounds.size)
        # TODO: Refine this calculation of border expansion
        if self._border > 1:
            bounds.inflate_ip(self._border*2, self._border*2)
        return bounds

    def _recalculate_offset(self):
        if self._transform_image is None:
            return
        size = self._scale * self._transform_image.get_size()
        offset = _anchor_offset(self._anchor, size[0], size[1])
        self._offset = Vec2D(offset) - self._transform_offset

    def _redraw_internal_image(self):
        # TODO: This should use math to calculate the angle/flip/scale instead of the pygame objects
        target = InternalImage(size=self._size)
        if not self._points or len(self._points) < 3:
            return self._make_blank_surface()
        origin = self._bounds.topleft
        # TODO: Refine this calculation of border expansion
        if self._border > 1:
            origin = origin + Vec2D(self._border, self._border)
        offset_points = [point-origin for point in self._points]
        pygame.draw.polygon(target._surf, _process_color(self._color),
                            offset_points, self._border)
        self._default_redraw_transforms(target)

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
        self._size = self._get_bounds()
        self._redraw_internal_image()

    @property
    def points(self):
        return self._points

    @points.setter
    def points(self, value):
        if len(value) % 2 == 0 and are_numbers(*value):
            value = list(zip(value[::2], value[1::2]))
        if not is_non_empty_iterable_of_points(value) or len(value) < 3:
            raise ValueError("The points of a shape must be a list of at least 3 points")
        self._points = value
        self._size = self._get_bounds()
        self._redraw_internal_image()


def shape(color, *points, x=None, y=None, anchor='center', border=None, filled=True, absolute=False):
    """
    Function to create a shape of at least three points.

    :param color: color of shape.
    :type color: str
    :param points: coordinates of points of shape
    :type points: List[Tuple] in (x, y), (x, y) format of points to be connected of shape
    :return: Shape object created
    """
    # Did they just pass in a list/tuple of points?
    if len(points) == 1 and isinstance(points[0], (list, tuple)):
        points = points[0]
    # Did they pass in a flat list of numbers (paired)?
    if len(points) % 2 == 0 and are_numbers(*points):
        points = list(zip(points[::2], points[1::2]))
    # Is the result a valid list of points?
    if not is_non_empty_iterable_of_points(points):
        print(points)
        raise ValueError("The points of a shape must be a list of at least 3 points.")
    # Must have at least three points
    if not at_least_three(points):
        raise ValueError("You need at least three points in your shape.")
    # And handle filling
    if filled is True:
        border = 0
    elif filled is False:
        border = border or Shape.DEFAULT_BORDER_WIDTH
    elif border is None:
        border = Shape.DEFAULT_BORDER_WIDTH
    return Shape((x, y), points, anchor, color, border, absolute)

def lines(color, *points, anchor='center', border=None, filled=True):
    return shape(color, *points, anchor=anchor, border=border, filled=filled, absolute=True)
