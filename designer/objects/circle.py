from designer.colors import _process_color
from designer.helpers import get_width, get_height
from designer.objects.designer_object import DesignerObject
from designer.core.internal_image import InternalImage, DesignerSurface
from designer.utilities import Vec2D
from designer.utilities.util import _anchor_offset


class Circle(DesignerObject):
    FIELDS = (*DesignerObject.FIELDS, 'radius', 'color', 'border')

    def __init__(self, color, radius, x=None, y=None, border=None, **kwargs):
        """
        Function to create a circle.

        >>> centered_circle = circle('red', 10)
        >>> positioned_circle = circle('blue', 20, 0, 0, anchor='topleft')
        >>> empty_circle = circle('black', 10, border=1)

        :param color: The color of the circle
        :param radius: The radius of the circle in pixels
        :param x: Defaults to center of screen if not given
        :param y: Defaults to center of screen if not given
        :param border:
        :return: Circle
        """
        super().__init__(**kwargs)

        if not isinstance(radius, (int, float)):
            raise ValueError(
                f"The parameter radius was given the value {radius!r} but that parameter must be either an integer or a float.")

        # Allow `x` as a tuple of positions
        if x is not None and y is None:
            if isinstance(x, (list, tuple, Vec2D)):
                x, y = x

        x = x if x is not None else get_width()/2
        y = y if y is not None else get_height()/2

        self._pos = x, y
        # Circle specific data
        self._radius = radius
        self._color = color
        self._border = border

        # And draw!
        self._redraw_internal_image()

    def __repr__(self):
        return f"<{self._active_status()}circle(color={self._color!r}, radius={self._radius}, x={self.x}, y={self.y})>"

    def __str__(self):
        return f"<{self._active_status()}circle({self._color!r}, {self._radius})>"

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


circle = Circle
