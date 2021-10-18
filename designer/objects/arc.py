import pygame

from designer.colors import _process_color
from designer.helpers import get_width, get_height
from designer.objects.designer_object import DesignerObject


class Arc(DesignerObject):
    def __init__(self, color, start_angle, stop_angle, thickness, left, top, width, height):
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
        super().__init__()
        self.dirty = 1
        color = _process_color(color)

        self.image = pygame.surface.Surface((width * 2, height * 2), pygame.SRCALPHA, 32).convert_alpha()
        pygame.draw.arc(self.image, color, (0, 0, width, height), start_angle, stop_angle, width=thickness)

        self.rect = self.image.get_rect()

        left = left if left is not None else get_width() / 2 - self.rect.width / 2
        top = top if top is not None else get_height() / 2 - self.rect.height / 2

        self.rect.x = left
        self.rect.y = top

        super().add()


def arc(color, start_angle, stop_angle, thickness, *args):
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
    if len(args) == 2:
        left, top = None, None
        width, height = args[2], args[3]
    elif len(args) > 2:
        left, top = args[0], args[1]
        width, height = args[2], args[3]
    else:
        left, top = args[0]
        width, height = args[1]
    return Arc(color, start_angle, stop_angle, thickness, left, top, width, height)