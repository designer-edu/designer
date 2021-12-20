import imghdr
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


class Image(DesignerObject):
    _USER_AGENT = "Designer Game Library for Python"
    FIELDS = (*DesignerObject.FIELDS, 'filename', 'image')
    _IMAGE_CACHE = {}
    _GIF_CACHE = {}

    def __init__(self, center, path, anchor, **kwargs):
        """
        Creates Image Designer Object on window

        :param center: x, y coordinates of center of circle
        :type center: Tuple[int]
        :param anchor: the anchor to draw the circle at
        :type anchor: str
        :param path: either url or local file path to image to load on screen
        :type path: str
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
        self._filename = path
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
        if self._filename in self._GIF_CACHE:
            # TODO: Return a copy instead?
            return self.animate(self._GIF_CACHE[self._filename])
        if self._filename in self._IMAGE_CACHE:
            self._internal_image = self._IMAGE_CACHE[self._filename].copy()
        try:
            path_strs = self._filename.split('/')
            fixed_paths = os.path.join(*path_strs)
            if os.path.exists(fixed_paths):
                if imghdr.what(fixed_paths) == 'gif':
                    with open(fixed_paths) as image_file:
                        gif = GifImage(image_file)
                        self.animate(gif)
                        self._GIF_CACHE[fixed_paths] = gif
                else:
                    self._internal_image = InternalImage(fixed_paths)
                    self._IMAGE_CACHE[fixed_paths] = self._internal_image
            else:
                raise FileNotFoundError(fixed_paths)
        except FileNotFoundError as err:
            try:
                req = Request(self._filename, headers={'User-Agent': self._USER_AGENT})
                with urlopen(req) as opened_image:
                    image_str = opened_image.read()
                    image_file = io.BytesIO(image_str)
                    if imghdr.what(None, h=image_str) == 'gif':
                        gif = GifImage(image_file)
                        self.animate(gif)
                        self._GIF_CACHE[self._filename] = gif
                    else:
                        self._internal_image = InternalImage(filename=self._filename, fileobj=image_file)
                        self._IMAGE_CACHE[self._filename] = self._internal_image
            except:
                if self._filename.startswith('https://') or self._filename.startswith('http://'):
                    raise ValueError(f"Unexpected error while loading url: {self._filename!r}")
                raise ValueError(f"Unexpected error while loading image from filename: {self._filename!r}")

    def _recalculate_offset(self):
        """
        Recalculates this designer object's offset based on its position, transform
        offset, anchor, its image, and the image's scaling.
        """
        if self._internal_image is None:
            return
        size = self._scale * self._internal_image.size
        offset = _anchor_offset(self._anchor, size[0], size[1])
        self._size = size
        self._offset = Vec2D(offset) - self._transform_offset

    def _redraw_internal_image(self):
        """
        Calculates the transforms that need to be applied to this designer object's
        image. In order: flipping, scaling, and rotation.
        """
        if self._internal_image is None:
            return
        source = self._internal_image._surf
        # Flip
        if self._flip_x or self._flip_y:
            source = pygame.transform.flip(source, self._flip_x, self._flip_y)
        # Scale
        if self._scale != (1.0, 1.0):
            new_size = self._scale * self._internal_image.size
            new_size = (int(new_size[0]), int(new_size[1]))
            if 0 in new_size:
                return self._make_blank_surface()
            new_surf = DesignerSurface(new_size)
            source = pygame.transform.smoothscale(source, new_size, new_surf)
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
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, value):
        if value == self._filename:
            return
        self._filename = value
        self._load_image()
        self._redraw_internal_image()
        self._recalculate_offset()
        self._expire_static()

    @property
    def image(self):
        return self._internal_image

    @image.setter
    def image(self, value):
        if isinstance(value, DesignerObject):
            self._internal_image = value._transform_image.copy()
            self._filename = None
            self._redraw_internal_image()
            self._recalculate_offset()
            self._expire_static()
            return
        if isinstance(value, pygame.Surface):
            value = InternalImage.from_surface(value)
        if not isinstance(value, InternalImage):
            return
        if value == self._internal_image and self._internal_image._version == value._version:
            return
        self._internal_image = value
        self._filename = value._name
        self._redraw_internal_image()
        self._recalculate_offset()
        self._expire_static()


def image(path, x=None, y=None, anchor='center', **kwargs):
    """
    Function to create an image.

    :param path: local file path or url of image to upload
    :type path: str
    :param args: left top corner of image and width and height of image
    :type args: two Tuples (left, top), (width, height) or four ints left, top, width, height
    :return: Image object
    """
    if x is not None and y is None:
        x, y = x
    return Image((x, y), path, anchor, **kwargs)

