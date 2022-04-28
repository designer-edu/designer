from typing import Optional, Union

import json
import pygame
import io

from designer.helpers import get_width, get_height
from designer.objects.designer_object import DesignerObject
from designer.core.internal_image import InternalImage
from designer.utilities import Vec2D
from designer.utilities.util import _anchor_offset


try:
    from zipfile import ZipFile
    from os import path
    _THIS_DIRECTORY = path.abspath(path.dirname(__file__))
    _UNICODE_LIST_PATH = path.join(_THIS_DIRECTORY, '../data/unicode_names.json')
    _EMOJI_DATABASE = path.join(_THIS_DIRECTORY, '../data/emojis.zip')
    ALT_MODE = False
except:
    # TODO: Emoji support limited in Skuplt
    ALT_MODE = True
    _UNICODE_LIST_PATH = 'src/lib/designer/data/unicode_names.json'

_UNICODE_LOOKUP = {}


def lookup_unicode(name):
    if not _UNICODE_LOOKUP:
        with open(_UNICODE_LIST_PATH) as unicode_list_file:
            _UNICODE_LOOKUP.update(json.load(unicode_list_file))
    return _UNICODE_LOOKUP[name.lower()].lower()


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
        super().__init__(**kwargs)

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
        self._svg: Optional[Union[str, dict]] = None
        #: Internal field holding the original version of the image
        self._internal_image: Optional[InternalImage] = None
        self._internal_image_version: Optional[int] = None

        self._load_image()

        # And draw!
        self._redraw_internal_image()
        self._recalculate_offset()

    def __repr__(self):
        activated = "" if self._active else "INACTIVE "
        name = self._name if len(self._name) < 40 else self._name[:40-3]+"..."
        return f"<{activated}emoji({name!r})>"

    def _get_unicode(self, text):
        # Look up the name or character
        try:
            return lookup_unicode(text)
        except KeyError:
            character = text
        try:
            return hex(ord(character))[2:]
        except TypeError:
            raise Exception(f"Unknown unicode name '{text}', could not find an emoji for this name.")

    def _load_image(self):
        if self._name in self._EMOJI_CACHE:
            self._svg = self._EMOJI_CACHE[self._name]
        target = self._get_unicode(self._name)
        try:
            emoji_database = ZipFile(_EMOJI_DATABASE)
            with emoji_database.open(target) as svg_file:
                self._svg = svg_file.read()
            self._EMOJI_CACHE[self._name] = self._svg
        except KeyError:
            raise Exception(f"Unknown unicode name '{self._name}', could not find an emoji for this name.")

    def _alt_load_image(self):
        target = self._get_unicode(self._name)
        # Hackish skulpt-specific solution for loading svgs in a special way
        self._svg = {'code': target}

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
        size = Vec2D(self.DEFAULT_EMOJI_SIZE, self.DEFAULT_EMOJI_SIZE) * self._scale
        l, r = size
        tx, ty = size/2
        flip_x, flip_y = "-" if self._flip_x else "", "-" if self._flip_y else ""
        # TODO: Mac's rotate incorrectly from topleft instead of center
        transforms = (f"translate({tx}, {ty}),"
                      f"rotate({self._angle}),"
                      f"translate({-tx}, {-ty}),"
                      f"scale({flip_x}{self._scale[0]}, {flip_y}{self._scale[1]})")
        image_data = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {l} {r}">'
                      f'<g transform="{transforms}">{self._svg}'
                      f'</g></svg>'.encode())
        image_file = io.BytesIO(image_data)
        # Renders it into the image
        self._internal_image = InternalImage(filename=self._name+".svg", fileobj=image_file)
        source = self._internal_image._surf
        # Finish updates
        self._transform_image = source
        self._recalculate_offset()
        self._expire_static()

    def _alt_redraw_internal_image(self):
        """
        Calculates the transforms that need to be applied to this designer object's
        image. In order: flipping, scaling, and rotation.

        This is the alternate version used by Skulpt.
        """
        self._svg['angle'] = self._angle
        self._svg['flip_x'] = "-" if self.flip_x else ""
        self._svg['flip_y'] = "-" if self.flip_y else ""
        self._svg['scale_x'] = self._scale[0]
        self._svg['scale_y'] = self._scale[1]
        self._svg['width'] = self.DEFAULT_EMOJI_SIZE #self._size[0]
        self._svg['height'] = self.DEFAULT_EMOJI_SIZE #self._size[1]
        # Renders it into the image
        self._internal_image = InternalImage(self._svg)
        source = self._internal_image._surf
        # Flip
        if self._flip_x or self._flip_y:
            source = pygame.transform.flip(source, self._flip_x, self._flip_y)
        # Scale
        #if self._scale != (1.0, 1.0):
        #    new_size = self._scale * self._internal_image.size
        #    new_size = (int(new_size[0]), int(new_size[1]))
        #    if 0 in new_size:
        #        return self._make_blank_surface()
        #    new_surf = DesignerSurface(new_size)
        #    source = pygame.transform.smoothscale(source, new_size, new_surf)
        # Rotate

        if self._angle != 0:
            angle = self._angle % 360
            old = Vec2D(source.get_rect().center)
            source = pygame.transform.rotate(source, angle).convert_alpha()
            new = source.get_rect().center
            self._transform_offset = old - new
        else:
            self._transform_offset = Vec2D(0, 0)

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


if ALT_MODE:
    Emoji._load_image = Emoji._alt_load_image
    Emoji._redraw_internal_image = Emoji._alt_redraw_internal_image


def get_emoji_name(an_emoji: Emoji) -> str:
    return an_emoji.name


def set_emoji_name(an_emoji: Emoji, new_name: str):
    an_emoji.name = new_name

