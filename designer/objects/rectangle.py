import pygame

from designer.colors import _process_color
from designer.helpers import get_width, get_height
from designer.objects.designer_object import DesignerObject

class Rectangle(DesignerObject):
    def __init__(self, left, top, width, height, color):
        """
        Creates Rectangle Designer Object on window.

        :param left: x position of top left corner of rectangle
        :type left: int
        :param top: y position of top left corner of rectangle
        :type top: int
        :param width: width of rectangle in pixels
        :type width: int
        :param height: height of rectangle in pixels
        :type height: int
        :param color: color of rectangle
        :type color: str or List[str]
        """
        super().__init__()
        self.dirty = 1
        color = _process_color(color)

        self.image = pygame.surface.Surface((width, height), pygame.SRCALPHA, 32).convert_alpha()
        pygame.draw.rect(self.image, color, (0, 0, width, height))

        self.color = color
        self.rect = self.image.get_rect()

        left = left if left is not None else get_width() / 2 - self.rect.width / 2
        top = top if top is not None else get_height() / 2 - self.rect.height / 2

        self.rect.topleft = (left, top)

        super().add()


def rectangle(color, *args):
    '''
    Function to create a rectangle.

    :param color: color of rectangle
    :type color: str or List[str]
    :param args: left top corner of image and width and height of rectangle
    :type args: two Tuples (left, top), (width, height) or four ints left, top, width, height
    :return: Rectangle object created
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
    return Rectangle(left, top, width, height, color)