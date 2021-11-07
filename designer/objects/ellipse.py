import math
import pygame

from designer.colors import _process_color
from designer.helpers import get_width, get_height
from designer.objects.designer_object import DesignerObject
from designer.core.internal_image import InternalImage, DesignerSurface
from designer.utilities.vector import Vec2D
from designer.utilities.util import _anchor_offset

class Ellipse(DesignerObject):
    DEFAULT_BORDER_WIDTH = 1
    FIELDS = (*DesignerObject.FIELDS, 'color', 'border')

    def __init__(self, center, width, height, anchor, color, border):
        '''
        Creates an ellipse Designer Object on the window.

        :param left: x coordinate of top left corner of ellipse
        :type left: int
        :param top: y coordinate of top left corner of ellipse
        :type top: int
        :param width: width of ellipse to be drawn
        :type width: int
        :param height: height of ellipse to be drawn
        :type height: int
        :param anchor: the anchor to draw the circle at
        :type anchor: str
        :param color: color of ellipse
        :type color: str or List[str]
        :param border: the width of the circle's line (0 is used for a filled circle)
        :type border: int
        '''
        super().__init__()

        x, y = center
        x = x if x is not None else get_width() / 2
        y = y if y is not None else get_height() / 2
        center = x, y

        self._pos = center
        self._anchor = anchor
        # Ellipse specific data
        self._size = Vec2D(width, height)
        self._color = color
        self._border = border

        # And draw!
        self._redraw_internal_image()

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
            target = InternalImage(size=(1, 1))
            target.fill(color)
            target = self._transform_image._surf
            self._recalculate_offset()
            self._expire_static()
            return
        new_image = InternalImage(size=size)
        new_image.draw_ellipse(color, (0, 0), size, self._border or 0)
        # Rotation
        if self._angle != 0:
            angle = self._angle % 360
            old = Vec2D(new_image.rect.center)
            source = pygame.transform.rotate(new_image._surf, angle).convert_alpha()
            new = source.rect.center
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


def ellipse(color, width=None, height=None, x=None, y=None, anchor='center', border=None):
    '''
    Function to make an ellipse.

    :param color: color of ellipse
    :type color: str or List[str]
    :return: Ellipse object created
    '''
    if x is not None and y is None:
        x, y = x
    elif x is None and y is None and height is not None:
        if not isinstance(height, (int, float)):
            x, y = height
            width, height = width
    elif height is None:
        width, height = width
    return Ellipse((x, y), width, height, anchor, color, border)
