from designer.colors import _process_color
from designer.helpers import get_width, get_height
from designer.objects.designer_object import DesignerObject
from designer.core.internal_image import InternalImage, DesignerSurface
from designer.utilities import Vec2D
from designer.utilities.util import _anchor_offset


class Circle(DesignerObject):
    DEFAULT_BORDER_WIDTH = 1
    FIELDS = (*DesignerObject.FIELDS, 'radius', 'color', 'border')

    def __init__(self, center, anchor, radius, color, border):
        """
        Creates a circle object on the window.

        :param center: x, y coordinates of center of circle
        :type center: Tuple[int]
        :param anchor: the anchor to draw the circle at
        :type anchor: str
        :param radius: The radius of the circle
        :type radius: int
        :param color: color of circle
        :type color: str or List[str]
        :param border: the width of the circle's line (0 is used for a filled circle)
        :type border: int
        """
        super().__init__()

        x, y = center
        x = x if x is not None else get_width()/2
        y = y if y is not None else get_height()/2
        center = x, y

        self._pos = center
        self._anchor = anchor
        # Circle specific data
        self._radius = radius
        self._color = color
        self._border = border

        # And draw!
        self._redraw_internal_image()

    def _recalculate_offset(self):
        size = 2 * self._radius * self.scale[0]
        offset = _anchor_offset(self._anchor, size, size)
        self._offset = Vec2D(offset) - self._transform_offset

    def _redraw_internal_image(self):
        radius = self._radius * self._scale[0]
        diameter = 2 * radius
        color = _process_color(self._color)
        if int(radius) > 0:
            new_image = InternalImage(size=(diameter, diameter))
            new_image.draw_circle(color, (radius, radius),
                                  radius, self._border or 0)
            target = new_image
        else:
            target = InternalImage(size=(1, 1))
            target.fill(color)
        self._transform_image = target._surf
        self._recalculate_offset()
        self._expire_static()

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        self._radius = value
        self._redraw_internal_image()

    @property
    def size(self):
        return Vec2D(self._radius, self._radius)

    @size.setter
    def size(self, value):
        if isinstance(value, (int, float)):
            self._radius = int(value)
        else:
            self._radius = value[0]
        self._redraw_internal_image()

    @property
    def width(self):
        return self._radius*2

    @width.setter
    def width(self, value):
        self._radius = value*2
        self._redraw_internal_image()

    @property
    def height(self):
        return self._radius*2

    @height.setter
    def height(self, value):
        self._radius = value*2
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


def circle(color, radius, x=None, y=None, anchor='center', border=None):
    """
    Function to create a circle.

    >>> centered_circle = circle('red', 10)
    >>> positioned_circle = circle('blue', 20, 0, 0, 'topleft')
    >>> empty_circle = circle('black', 10, filled=False)

    :param x:
    :param y:
    :param filled:
    :param border:
    :param anchor:
    :param color: color of circle
    :param radius: int, radius of circle in pixels
    :return: Circle object created
    """
    if not isinstance(radius, (int, float)):
        raise ValueError(f"The parameter radius was given the value {radius!r} but that parameter must be either an integer or a float.")
    if x is not None and y is None:
        x, y = x
    return Circle((x, y), anchor, radius, color, border)
