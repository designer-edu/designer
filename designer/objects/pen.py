import pygame

from collections import deque

from designer import register
from designer.objects.designer_object import DesignerObject
from designer.colors import _process_color
from designer.helpers import get_width, get_height
from designer.core.internal_image import InternalImage, DesignerSurface
from designer.utilities.vector import Vec2D
from designer.utilities.util import _anchor_offset, rect_from_points
from designer.utilities.animation import *
from designer.utilities.easings import Linear, Iterate, Random, LinearTuple
from designer.utilities.rect import Rect


class Pen(DesignerObject):
    """
    TODO: Finish this with the idea of iteratively "painting" on a canvas.

    """

    def __init__(self, center, thickness, color, speed):
        super().__init__()

        x, y = center
        x = x if x is not None else get_width() / 2
        y = y if y is not None else get_height() / 2
        center = Vec2D(x, y)

        self._pos = center
        # Pen specific data
        self._color = color
        self._thickness = thickness
        self._inking = True
        self._speed = speed
        # The points we have visited
        self._pen_pos = center
        self._visited_points = []
        self._bounds = self._get_bounds()
        self._size = self._bounds.size
        self._current_animation = None
        self._queued_animations = deque()
        self._speed = 4

        # And draw!
        self._redraw_internal_image()

        register('Pen.pen_pos.animation.start', self._visit_point)
        register('Pen.pen_pos.animation.end', self._finish_point)

    def _restart_animation_if_needed(self):
        if not self._current_animation and self._queued_animations:
            x, y, speed = self._queued_animations.popleft()
            print(self._pen_pos, (x, y), speed)
            self._current_animation = Animation('pen_pos', LinearTuple(self._pen_pos, (x, y)), self._speed)
            self._speed += 1
            self.animate(self._current_animation)

    @property
    def pen_pos(self):
        """
        The position of a sprite in 2D coordinates, represented as a
        :class:`Vec2D <spyral.Vec2D>`
        """
        return self._pen_pos

    @pen_pos.setter
    def pen_pos(self, value):
        if value == self._pen_pos:
            return
        self._pen_pos = Vec2D(value)
        self._bounds = self._get_bounds()
        self._pos = self._bounds.topleft
        self._size = self._bounds.size
        self._redraw_internal_image()
        self._expire_static()

    def move_to(self, x, y, speed=None):
        if speed is None:
            speed = self._speed
        self._queued_animations.append((x, y, speed))
        self._restart_animation_if_needed()

    def _visit_point(self):
        self._visited_points.append(Vec2D(self._pen_pos))
        self._bounds = self._get_bounds()
        self._size = self._bounds.size
        self._redraw_internal_image()

    def _finish_point(self):
        self._current_animation = None
        self._restart_animation_if_needed()

    def _get_bounds(self):
        if not self._visited_points:
            return Rect(self._pen_pos.x, self._pen_pos.y, 1, 1)
        bounds = rect_from_points(self._visited_points + [self._pen_pos])
        # TODO: Refine this calculation of border expansion
        if self._thickness > 0:
            bounds.inflate_ip(self._thickness*2, self._thickness*2)
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
        points = self._visited_points + [self._pen_pos]
        if len(points) <= 1:
            return self._make_blank_surface()
        origin = self._bounds.topleft
        # TODO: Refine this calculation of border expansion
        if self._thickness > 1:
            origin = origin + Vec2D(self._thickness, self._thickness)
        offset_points = [point-origin for point in points]
        pygame.draw.lines(target._surf, _process_color(self._color), False,
                            offset_points, self._thickness)
        self._default_redraw_transforms(target)


def pen(color='black', x=None, y=None, thickness=1, speed=2):
    return Pen((x, y), thickness, color, speed)
