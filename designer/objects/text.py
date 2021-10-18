import pygame

from designer.colors import _process_color
from designer.helpers import get_width, get_height
from designer.objects.designer_object import DesignerObject


class Text(DesignerObject):
    __initialized = False
    def __init__(self, left, top, text_color, text, text_size):
        """
        Creates Text Designer Object on window

        :param left: x coordinate of top left corner of text box
        :type left: int
        :param top: y coordinate of top left corner of text box
        :type top: int
        :param text_color: color of text
        :type text_color: str or List[str]
        :param text: text to be written on window
        :type text: str
        :param text_size: font size of text
        :type text_size: int
        """
        super().__init__()
        self.dirty = 1
        text_color = _process_color(text_color)

        # is there a way to load text quicker?
        # TODO: Cache this font
        self.font = pygame.font.SysFont('Arial', text_size)

        #  self.image = pygame.surface.Surface((width, height), pygame.SRCALPHA, 32).convert_alpha()
        self.text = text
        self.text_color = text_color
        self.image = self.font.render(self.text, True, self.text_color)
        self.rect = self.image.get_rect()

        left = left if left is not None else get_width() / 2 - self.rect.width / 2
        top = top if top is not None else get_height() / 2 - self.rect.height / 2
        self.rect.topleft = (left, top)

        self.__initialized = True

        super().add()

    def __setattr__(self, name, value):
        old_value = None
        if self.__initialized:
            old_value = getattr(self, name)
        super().__setattr__(name, value)
        if self.__initialized and name == 'text' and old_value != value:
            self.image = self.font.render(value, True, self.text_color)
            self.rect.size = self.image.get_size()
            self.dirty = 1


def text(text_color, text, text_size, *args):
    '''
       Function to create text.

       :param color: color of text
       :type color: str or List[str]
       :param text: text to appear on window
       :type text: str
       :param args: top left coordinates of text box
       :type args: either Tuple (left, top) or two ints (left, top)
       :return: Text object created
       '''
    if not args:
        left, top = None, None
    elif len(args) >= 2:
        left, top = args[0], args[1]
    else:
        left, top = args[0]
    return Text(left, top, text_color, text, text_size)