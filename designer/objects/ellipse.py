import pygame

from designer.colors import _process_color
from designer.helpers import get_width, get_height
from designer.objects.designer_object import DesignerObject


class Ellipse(DesignerObject):
    def __init__(self, color, left, top, width, height):
        '''
        Creates an ellipse Designer Object on the window.

        :param color: color of ellipse
        :type color: str or List[str]
        :param left: x coordinate of top left corner of ellipse
        :type left: int
        :param top: y coordinate of top left corner of ellipse
        :type top: int
        :param width: width of ellipse to be drawn
        :type width: int
        :param height: height of ellipse to be drawn
        :type height: int
        '''
        super().__init__()
        self.dirty = 1
        color = _process_color(color)

        self.image = pygame.surface.Surface((2 * width, 2 * height), pygame.SRCALPHA, 32).convert_alpha()
        pygame.draw.ellipse(self.image, color, (0, 0, width, height))

        self.rect = self.image.get_rect()

        left = left if left is not None else get_width() / 2 - self.rect.width / 2
        top = top if top is not None else get_height() / 2 - self.rect.height / 2

        self.rect.x = left
        self.rect.y = top

        super().add()


def ellipse(color, *args):
    '''
    Function to make an ellipse.

    :param color: color of ellipse
    :type color: str or List[str]
    :param args: left top corner of ellipse and width and height of ellipse
    :type args: two Tuples (left, top), (width, height) or four ints left, top, width, height
    :return: Ellipse object created
    '''
    if len(args) == 2:
        left, top = None, None
        width, height = args[0], args[1]
    elif len(args) > 2:
        left, top = args[0], args[1]
        width, height = args[2], args[3]
    else:
        left, top = args[0]
        width, height = args[1]
    return Ellipse(color, left, top, width, height)