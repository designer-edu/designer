from designer.colors import _process_color
from designer.helpers import get_width, get_height
from designer.objects.designer_object import DesignerObject
from designer.core.internal_image import InternalImage
from designer.utilities.surfaces import DesignerSurface


class Circle(DesignerObject):
    DEFAULT_BORDER_WIDTH = 1

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

        self.pos = center
        self.anchor = anchor
        # Circle specific data
        self._radius = radius
        self._color = color
        self._border = border
        # Draw the actual circle image
        self._internal_image = self._redraw_internal_image()
        self._transform_image = self._internal_image._surf

    def _redraw_internal_image(self):
        radius = self._radius * self._scale[0]
        if int(radius) > 0:
            new_image = InternalImage(size=(2 * radius, 2 * radius))
            new_image.draw_circle(_process_color(self._color), (radius, radius),
                                             radius, self._border)
            return new_image
        else:
            return InternalImage(size=(1, 1))

    def _recalculate_transforms(self):
        """
        Calculates the transforms that need to be applied to this designer object's
        image. In order: flipping, scaling, and rotation.
        """
        source = self._internal_image
        # Scale
        if self._scale != (1.0, 1.0):
            new_size = self._scale * self._radius
            new_size = (int(new_size[0]), int(new_size[1]))
            if 0 in new_size:
                self._transform_image = DesignerSurface((1, 1))
                self._recalculate_offset()
                self._expire_static()
                return
            source = self._redraw_internal_image()
        # Finish updates
        self._transform_image = source._surf
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


def circle(color, radius, x=None, y=None, anchor='center', border=None, filled=True):
    """
    Function to create a circle.

    >>> centered_circle = circle('red', 10)
    >>> positioned_circle = circle('blue', 20, 0, 0, 'topleft')
    >>> empty_circle = circle('black', 10, filled=False)

    :param color: color of circle
    :param radius: int, radius of circle in pixels
    :return: Circle object created
    """
    if x is not None and y is None:
        x, y = x
    if filled is True:
        border = 0
    elif filled is False:
        border = border or Circle.DEFAULT_BORDER_WIDTH
    elif border is None:
        border = Circle.DEFAULT_BORDER_WIDTH
    return Circle((x, y), anchor, radius, color, border)
