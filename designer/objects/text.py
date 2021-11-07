import pygame
import math

from designer.colors import _process_color
from designer.helpers import get_width, get_height
from designer.objects.designer_object import DesignerObject
from designer.core.internal_image import InternalImage, DesignerSurface
from designer.utilities.vector import Vec2D
from designer.utilities.util import _anchor_offset

class Text(DesignerObject):
    DEFAULT_FONT_SIZE = 16
    DEFAULT_FONT_COLOR = 'black'
    DEFAULT_FONT_NAME = 'Arial'
    FONTS = {}
    FIELDS = (*DesignerObject.FIELDS, 'text', 'color', 'font', 'text_size')

    def __init__(self, center, anchor, text_string, text_size, color, font):
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

        self._pos = center
        self._anchor = anchor
        # Text Specific data
        self._text = text_string
        self._text_size = text_size
        self._color = color
        self._font_name = font
        self._update_font()

        # Draw the actual circle image
        self._redraw_internal_image()

    def _recalculate_offset(self):
        if self._transform_image is None:
            return
        size = self._scale * self._transform_image.get_size()
        offset = _anchor_offset(self._anchor, size[0], size[1])
        self._offset = Vec2D(offset) - self._transform_offset

    def _redraw_internal_image(self):
        text_surface = self._font.render(str(self.text), True, _process_color(self.color))
        target = InternalImage(size=text_surface.get_size())
        target._surf.blit(text_surface, (0, 0))
        self._default_redraw_transforms(target)

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
        self._text = value
        self._redraw_internal_image()


def text(color, text, text_size=Text.DEFAULT_FONT_SIZE,
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
        try:
            x, y = x
        except TypeError as e:
            pass
    return Text((x, y), anchor, text, text_size, color, font_name)