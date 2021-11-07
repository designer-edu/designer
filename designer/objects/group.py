import imghdr
from typing import Optional

import pygame
import math

from designer.colors import _process_color
from designer.helpers import get_width, get_height
from designer.objects.designer_object import DesignerObject
from designer.core.internal_image import InternalImage, DesignerSurface
from designer.utilities import Vec2D, Rect
from designer.utilities.util import _anchor_offset
from designer.objects.image import Image


class DesignerGroup(DesignerObject):
    '''
    class consisting of group of DesignerObjects together to allow
    collective functionality
    '''

    FIELDS = (*DesignerObject.FIELDS, )

    def __init__(self, objects):
        """
        Creates Image Designer Object on window

        :param center: x, y coordinates of center of circle
        :type center: Tuple[int]
        """
        super().__init__()

        boxes = [
            Rect(object._pos, object._transform_image.get_size())
            for object in objects
        ]
        if boxes:
            combined = boxes[0]
            for other in boxes[1:]:
                combined = combined.union(other)
            center = combined.center
            topleft = combined.topleft
            size = combined.size
        else:
            center = get_width(), get_height()
            size = 1, 1
            topleft = center

        self._pos = center
        self._anchor = 'center'
        self._size = size
        #: Internal field holding the original version of the image
        self._internal_image: Optional[InternalImage] = InternalImage(size=(size))
        self._internal_image_version: Optional[int] = None

        for object in objects:
            self._internal_image._surf.blit(object._transform_image, object.pos - topleft)
            self._internal_image_version = 1

        # And draw!
        self._redraw_internal_image()

    def _recalculate_offset(self):
        """
        Recalculates this designer object's offset based on its position, transform
        offset, anchor, its image, and the image's scaling.
        """
        if self._internal_image is None:
            return
        size = self._scale * self._internal_image.size
        offset = _anchor_offset(self._anchor, size[0], size[1])
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
        # Finish updates
        self._transform_image = source
        self._recalculate_offset()
        self._expire_static()


def flatten(objects):
    if isinstance(objects, (list, tuple)):
        result = []
        for r in objects:
            result.extend(flatten(r))
        return result
    else:
        return [objects]


def group(*objects):
    '''
    Function to group multiple objects together.

    :param objects: collection of objects to be grouped together for collective functionality
    :type objects: at least one DesignerObject
    :return: Created Designer Group object
    '''
    return DesignerGroup(flatten(objects))
