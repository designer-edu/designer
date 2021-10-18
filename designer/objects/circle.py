import pygame

from designer.colors import _process_color
from designer.helpers import get_width, get_height
from designer.objects.designer_object import DesignerObject


class Circle(DesignerObject):
    def __init__(self, center, size, color):
        """
        Creates a circle object on the window.

        :param center: x, y coordinates of center of circle
        :type center: Tuple[int]
        :param size: radius of circle
        :type size: int
        :param color: color of circle
        :type color: str or List[str]

        """
        super().__init__()
        self.dirty = 1
        color = _process_color(color)
        self.image = pygame.surface.Surface((2 * size, 2 * size), pygame.SRCALPHA, 32).convert_alpha()
        pygame.draw.circle(self.image, color, (size, size), size)

        x, y = center
        x = x if x is not None else get_width()/2 - size/2
        y = y if y is not None else get_height() / 2 - size / 2
        center = x, y

        self.center = center
        self.size = size
        self.color = color

        self.rect = self.image.get_rect(center=center)

        super().add()


def circle(color, radius, *args):
    """
    Function to create a circle.

    :param color: color of circle
    :param radius: int, radius of circle in pixels
    :param args: center of circle in x, y either as separate ints or as a tuple of ints
    :return: Circle object created
    """
    if len(args) == 0:
        x, y = None, None
    elif len(args) >= 2:
        x, y = args[0], args[1]
    else:
        x, y = args[0]
    return Circle((x, y), radius, color)
