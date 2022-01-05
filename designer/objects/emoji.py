from typing import Optional

from urllib.request import urlopen, Request
import pygame
import math
import sys
import os
import io

from designer.colors import _process_color
from designer.helpers import get_width, get_height
from designer.objects.designer_object import DesignerObject
from designer.core.internal_image import InternalImage, DesignerSurface
from designer.utilities import Vec2D
from designer.utilities.util import _anchor_offset
from designer.utilities.gif_image import GifImage

try:
    import unicodedata
    from zipfile import ZipFile
    from os import path
    _THIS_DIRECTORY = path.abspath(path.dirname(__file__))
    _EMOJI_DATABASE = path.join(_THIS_DIRECTORY, '../data/emojis.zip')
except:
    # TODO: Emoji support limited in Skuplt
    pass


OTHER_KNOWN_EMOJI = {
    "Kiss (dark skin tone person, medium-dark skin tone person)": "1f9d1-1f3ff-200d-2764-fe0f-200d-1f48b-200d-1f9d1-1f3fe"
    # TODO: Finish this list!
}


class Emoji(DesignerObject):
    FIELDS = (*DesignerObject.FIELDS, 'name')
    DEFAULT_EMOJI_SIZE = 36
    _EMOJI_CACHE = {}

    def __init__(self, center, name, anchor, **kwargs):
        """
        Creates Image Designer Object on window

        :param center: x, y coordinates of center of circle
        :type center: Tuple[int]
        :param anchor: the anchor to draw the circle at
        :type anchor: str
        :param name: The name of the emoji
        :type name: str
        :param width: width of image in pixels
        :type width: int
        :param height: height of image in pixels
        :type height: int
        """
        super().__init__()

        x, y = center
        x = x if x is not None else get_width() / 2
        y = y if y is not None else get_height() / 2
        center = x, y

        self._pos = center
        self._anchor = anchor
        # Image specific data
        self._size = Vec2D(self.DEFAULT_EMOJI_SIZE, self.DEFAULT_EMOJI_SIZE)
        self._name = name
        # Internal field holding the raw svg information
        self._svg: Optional[str] = None
        #: Internal field holding the original version of the image
        self._internal_image: Optional[InternalImage] = None
        self._internal_image_version: Optional[int] = None

        self._load_image()

        for key, value in kwargs.items():
            self[key] = value

        # And draw!
        self._redraw_internal_image()
        self._recalculate_offset()

    def _load_image(self):
        if self._name in self._EMOJI_CACHE:
            self._svg = self._EMOJI_CACHE[self._name]
        # Look up the name or character
        try:
            character = unicodedata.lookup(self._name)
        except KeyError:
            character = self._name
        try:
            target = hex(ord(character))[2:]
        except TypeError:
            target = OTHER_KNOWN_EMOJI.get(character, character)
        try:
            emoji_database = ZipFile(_EMOJI_DATABASE)
            with emoji_database.open(target) as svg_file:
                self._svg = svg_file.read()
            self._EMOJI_CACHE[self._name] = self._svg
        except KeyError:
            raise Exception(f"Unknown unicode name '{self._name}', could not find an emoji for this name.")

    def _recalculate_offset(self):
        """
        Recalculates this designer object's offset based on its position, transform
        offset, anchor, its image, and the image's scaling.
        """
        if self._internal_image is None:
            return
        size = self._internal_image.size
        offset = _anchor_offset(self._anchor, size[0], size[1])
        self._size = size
        self._offset = Vec2D(offset) - self._transform_offset

    def _redraw_internal_image(self):
        """
        Calculates the transforms that need to be applied to this designer object's
        image. In order: flipping, scaling, and rotation.
        """
        # Transform the SVG
        #  viewBox="0 0 36 36"
        flip_x, flip_y = "-" if self._flip_x else "", "-" if self._flip_y else ""
        transforms = f"rotate({self._angle})\nscale({flip_x}{self._scale[0]}, {flip_y}{self._scale[1]})"
        image_data = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self._size[0]} {self._size[1]}">'
                      f'<g transform="{transforms}">{self._svg}'
                      f'</g></svg>'.encode())
        image_file = io.BytesIO(image_data)
        # Renders it into the image
        self._internal_image = InternalImage(filename=self._name+".svg", fileobj=image_file)
        source = self._internal_image._surf
        # Updates angle
        #angle = self._angle % 360
        #old = Vec2D(source.get_rect().topleft)
        #new = old.rotated(angle)
        #self._transform_offset = old - new
        # Finish updates
        self._transform_image = source
        self._recalculate_offset()
        self._expire_static()

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if value == self._name:
            return
        self._name = value
        self._load_image()
        self._redraw_internal_image()
        self._recalculate_offset()
        self._expire_static()


def emoji(name, x=None, y=None, anchor='center', **kwargs):
    """
    Function to create an image from the emoji with the given name.

    :param name: The emoji's name
    :type name: str
    :param args: left top corner of image and width and height of image
    :type args: two Tuples (left, top), (width, height) or four ints left, top, width, height
    :return: Image object
    """
    if x is not None and y is None:
        if isinstance(x, (list, tuple)):
            x, y = x
    return Emoji((x, y), name, anchor, **kwargs)
