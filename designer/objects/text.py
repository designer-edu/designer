import pygame
import math

from designer.colors import _process_color
from designer.helpers import get_width, get_height
from designer.objects.designer_object import DesignerObject
from designer.core.internal_image import InternalImage
from designer.utilities.vector import Vec2D
from designer.utilities.surfaces import DesignerSurface


class Text(DesignerObject):
    DEFAULT_FONT_SIZE = 16
    DEFAULT_FONT_COLOR = 'black'
    DEFAULT_FONT_NAME = 'Arial'
    FONTS = {}

    def __init__(self, center, anchor, text, text_size, color, font):
        """
        Creates Text Designer Object on window

        :param center: x, y coordinates of center of circle
        :type center: Tuple[int]
        :param anchor: the anchor to draw the circle at
        :type anchor: str
        :param color: color of text
        :type color: str or List[str]
        :param text: text to be written on window
        :type text: str
        :param text_size: font size of text
        :type text_size: int
        """
        super().__init__()

        x, y = center
        x = x if x is not None else get_width() / 2
        y = y if y is not None else get_height() / 2
        center = x, y

        self.pos = center
        self.anchor = anchor
        # Text Specific data
        self._text = text
        self._text_size = text_size
        self._color = color
        self._font_name = font
        self._update_font()

        # Draw the actual circle image
        self._internal_image = self._redraw_internal_image()
        self._transform_image = self._internal_image._surf

    def _redraw_internal_image(self):
        text_surface = self._font.render(str(self.text), True, _process_color(self.color))
        target = InternalImage(size=text_surface.get_size())
        target._surf.blit(text_surface, (0, 0))
        return target

    @classmethod
    def _get_font(cls, font, text_size):
        if (font, text_size) not in cls.FONTS:
            cls.FONTS[(font, text_size)] = pygame.font.SysFont(font, text_size)
        return cls.FONTS[(font, text_size)]

    def _update_font(self):
        self._font = self._get_font(self._font_name, self._text_size)

    @property
    def text_size(self):
        return self._text_size

    @text_size.setter
    def text_size(self, value):
        self._text_size = value
        self._update_font()
        self._redraw_internal_image()

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = value
        self._redraw_internal_image()

    @property
    def font(self):
        return self._font

    @font.setter
    def font(self, value):
        self._font_name = value
        self._update_font()
        self._redraw_internal_image()

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = text
        self._redraw_internal_image()

def text(text, color=Text.DEFAULT_FONT_COLOR, text_size=Text.DEFAULT_FONT_SIZE,
         x=None, y=None, anchor='center', font_name=Text.DEFAULT_FONT_NAME):
    '''
       Function to create text.

       :param text: text to appear on window
       :type text: str
       :param color: color of text
       :type color: str or List[str]
       :return: Text object created
       '''
    if x is not None and y is None:
        x, y = x
    return Text((x, y), anchor, text, text_size, color, font_name)