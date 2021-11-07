import pygame
import copy
import imghdr
import math

from designer.utilities.vector import Vec2D
from designer.utilities.rect import Rect
from designer.utilities.util import scale_surface


class DesignerSurface(pygame.Surface):
    """
    Internal method for creating a DesignerSurface, which is just a Pygame
    Surface with the proper full SRCALPHA, 32 bits, and alpha transparency.
    """
    def __init__(self, size):
        super().__init__((int(size[0]), int(size[1])), pygame.SRCALPHA, 32)
        self.convert_alpha()


def from_sequence(images, orientation="right", padding=0):
    """
    A function that returns a new Image from a list of images by
    placing them next to each other.

    :param images: A list of images to lay out.
    :type images: List of :class:`Image <spyral.Image>`
    :param str orientation: Either 'left', 'right', 'above', 'below', or
                            'square' (square images will be placed in a grid
                            shape, like a chess board).
    :param padding: The padding between each image. Can be specified as a
                    scalar number (for constant padding between all images)
                    or a list (for different paddings between each image).
    :type padding: int or a list of ints.
    :returns: A new :class:`Image <spyral.Image>`
    """
    if orientation == 'square':
        length = int(math.ceil(math.sqrt(len(images))))
        max_height = 0
        sequence = []
        x, y = 0, 0
        for index, image in enumerate(images):
            if index % length == 0:
                x = 0
                y += max_height
                max_height = 0
            else:
                x += image.width
                max_height = max(max_height, image.height)
            sequence.append((image, (x, y)))
    else:
        if orientation in ('left', 'right'):
            selector = Vec2D(1, 0)
        else:
            selector = Vec2D(0, 1)

        if orientation in ('left', 'above'):
            reversed(images)
            # TODO: Does this actually do anything?

        if type(padding) in (float, int):
            padding = [padding] * len(images)
        else:
            padding = list(padding)
            padding.append(0)
        base = Vec2D(0, 0)
        sequence = []
        for image, padding in zip(images, padding):
            sequence.append((image, base))
            base = base + selector * (image.size + (padding, padding))
    return from_conglomerate(sequence)


def from_conglomerate(sequence):
    """
    A function that generates a new InternalImage from a sequence of
    (image, position) pairs. These images will be placed onto a singe image
    large enough to hold all of them. More explicit and less convenient than
    :func:`from_seqeuence <spyral.image.from_sequence>`.

    :param sequence: A list of (image, position) pairs, where the positions
                     are :class:`Vec2D <spyral.Vec2D>` s.
    :type sequence: List of image, position pairs.
    :returns: A new :class:`Image <spyral.Image>`
    """
    width, height = 0, 0
    for image, (x, y) in sequence:
        width = max(width, x+image.width)
        height = max(height, y+image.height)
    new = InternalImage(size=(width, height))
    for image, (x, y) in sequence:
        new.draw_internal_image(image, (x, y))
    return new

class InternalImage(object):
    """
    The InternalImage is the basic drawable item in designer. They can be created
    either by loading from common file formats, or by creating a new
    InternalImage and using some of the draw methods. InternalImages are not drawn on
    their own, they are placed as the *internal_image* attribute on DesignerObjects to
    be drawn.

    Almost all of the methods of an InternalImage instance return the InternalImage itself,
    enabling commands to be chained in a
    `fluent interface <http://en.wikipedia.org/wiki/Fluent_interface>`_.

    :param size: If size is passed, creates a new blank internal_image of that size to
                 draw on. If you do not specify a size, you *must* pass in a
                 filename.
    :type size: :class:`Vec2D <spyral.Vec2D>`
    :param str filename:  If filename is set, the file with that name is loaded.
                          The appendix has a list of the
                          :ref:`valid image formats<ref.image_formats>`. If you do
                          not specify a filename, you *must* pass in a size.

    """

    def __init__(self, filename=None, size=None, fileobj=None):
        if size is not None and filename is not None:
            raise ValueError("Must specify exactly one of size and filename. See http://platipy.org/en/latest/spyral_docs.html#spyral.internal_image.InternalImage")
        if size is None and filename is None:
            raise ValueError("Must specify exactly one of size and filename. See http://platipy.org/en/latest/spyral_docs.html#spyral.internal_image.InternalImage")

        if size is not None:
            self._surf = DesignerSurface(size)
            self._name = None
        else:
            self._name = filename
            if fileobj is None:
                fileobj = filename
            self._surf = pygame.image.load(fileobj).convert_alpha()
        self._version = 1

    def _get_width(self):
        return self._surf.get_width()

    #: The width of this internal_image in pixels (int). Read-only.
    width = property(_get_width)

    def _get_height(self):
        return self._surf.get_height()

    #: The height of this internal_image in pixels (int). Read-only.
    height = property(_get_height)

    def _get_size(self):
        return Vec2D(self._surf.get_size())

    #: The (width, height) of the internal_image (:class:`Vec2D <spyral.Vec2D`).
    #: Read-only.
    size = property(_get_size)

    @property
    def rect(self):
        return self._surf.get_rect()

    def fill(self, color):
        """
        Fills the entire internal_image with the specified color.

        :param color: a three-tuple of RGB values ranging from 0-255. Example:
                      (255, 128, 0) is orange.
        :type color: a three-tuple of ints.
        :returns: This internal_image.
        """
        self._surf.fill(color)
        self._version += 1
        scale_surface.clear(self._surf)
        return self

    def draw_rect(self, color, position, size=None,
                  border_width=0, anchor='topleft'):
        """
        Draws a rectangle on this internal_image.

        :param color: a three-tuple of RGB values ranging from 0-255. Example:
                      (255, 128, 0) is orange.
        :type color: a three-tuple of ints.
        :param position: The starting position of the rect (top-left corner). If
                         position is a Rect, then size should be `None`.
        :type position: :class:`Vec2D <spyral.Vec2D>` or
                        :class:`Rect <spyral.Rect>`
        :param size: The size of the rectangle; should not be given if position
                     is a rect.
        :type size: :class:`Vec2D <spyral.Vec2D>`
        :param int border_width: The width of the border to draw. If it is 0,
                                 the rectangle is filled with the color
                                 specified.
        :param str anchor: The anchor parameter is an
                           :ref:`anchor position <ref.anchors>`.
        :returns: This internal_image.
        """
        if size is None:
            rect = Rect(position)
        else:
            rect = Rect(position, size)
        offset = self._calculate_offset(anchor, rect.size)
        pygame.draw.rect(self._surf, color,
                             (rect.pos + offset, rect.size), border_width)
        self._version += 1
        scale_surface.clear(self._surf)
        return self

    def draw_lines(self, color, points, width=1, closed=False):
        """
        Draws a series of connected lines on a internal_image, with the
        vertices specified by points. This does not draw any sort of
        end caps on lines.

        :param color: a three-tuple of RGB values ranging from 0-255. Example:
                      (255, 128, 0) is orange.
        :type color: a three-tuple of ints.
        :param points: A list of points that will be connected, one to another.
        :type points: A list of :class:`Vec2D <spyral.Vec2D>` s.
        :param int width: The width of the lines.
        :param bool closed: If closed is True, the first and last point will be
                            connected. If closed is True and width is 0, the
                            shape will be filled.
        :returns: This internal_image.
        """
        if width == 1:
            pygame.draw.aalines(self._surf, color, closed, points)
        else:
            pygame.draw.lines(self._surf, color, closed, points, width)
        self._version += 1
        scale_surface.clear(self._surf)
        return self

    def draw_circle(self, color, position, radius, width=0, anchor='topleft'):
        """
        Draws a circle on this internal_image.

        :param color: a three-tuple of RGB values ranging from 0-255. Example:
                      (255, 128, 0) is orange.
        :type color: a three-tuple of ints.
        :param position: The center of this circle
        :type position: :class:`Vec2D <spyral.Vec2D>`
        :param int radius: The radius of this circle
        :param int width: The width of the circle. If it is 0, the circle is
                          filled with the color specified.
        :param str anchor: The anchor parameter is an
                           :ref:`anchor position <ref.anchors>`.
        :returns: This internal_image.
        """
        offset = self._calculate_offset(anchor)
        pygame.draw.circle(self._surf, color, (position + offset).floor(),
                           radius, width)
        self._version += 1
        scale_surface.clear(self._surf)
        return self

    def draw_ellipse(self, color, position, size=None,
                     border_width=0, anchor='topleft'):
        """
        Draws an ellipse on this internal_image.

        :param color: a three-tuple of RGB values ranging from 0-255. Example:
                      (255, 128, 0) is orange.
        :type color: a three-tuple of ints.
        :param position: The starting position of the ellipse (top-left corner).
                         If position is a Rect, then size should be `None`.
        :type position: :class:`Vec2D <spyral.Vec2D>` or
                        :class:`Rect <spyral.Rect>`
        :param size: The size of the ellipse; should not be given if position is
                     a rect.
        :type size: :class:`Vec2D <spyral.Vec2D>`
        :param int border_width: The width of the ellipse. If it is 0, the
                          ellipse is filled with the color specified.
        :param str anchor: The anchor parameter is an
                           :ref:`anchor position <ref.anchors>`.
        :returns: This internal_image.
        """
        if size is None:
            rect = Rect(position)
        else:
            rect = Rect(position, size)
        offset = self._calculate_offset(anchor, rect.size)
        pygame.draw.ellipse(self._surf, color,
                            (rect.pos + offset, rect.size), border_width)
        self._version += 1
        scale_surface.clear(self._surf)
        return self

    def draw_point(self, color, position, anchor='topleft'):
        """
        Draws a point on this internal_image.

        :param color: a three-tuple of RGB values ranging from 0-255. Example:
                      (255, 128, 0) is orange.
        :type color: a three-tuple of ints.
        :param position: The position of this point.
        :type position: :class:`Vec2D <spyral.Vec2D>`
        :param str anchor: The anchor parameter is an
                           :ref:`anchor position <ref.anchors>`.
        :returns: This internal_image.
        """
        offset = self._calculate_offset(anchor)
        self._surf.set_at(position + offset, color)
        self._version += 1
        scale_surface.clear(self._surf)
        return self

    def draw_arc(self, color, start_angle, end_angle,
                 position, size=None, border_width=0, anchor='topleft'):
        """
        Draws an elliptical arc on this internal_image.

        :param color: a three-tuple of RGB values ranging from 0-255. Example:
                      (255, 128, 0) is orange.
        :type color: a three-tuple of ints.
        :param float start_angle: The starting angle, in radians, of the arc.
        :param float end_angle: The ending angle, in radians, of the arc.
        :param position: The starting position of the ellipse (top-left corner).
                         If position is a Rect, then size should be `None`.
        :type position: :class:`Vec2D <spyral.Vec2D>` or
                        :class:`Rect <spyral.Rect>`
        :param size: The size of the ellipse; should not be given if position is
                     a rect.
        :type size: :class:`Vec2D <spyral.Vec2D>`
        :param int border_width: The width of the ellipse. If it is 0, the
                          ellipse is filled with the color specified.
        :param str anchor: The anchor parameter is an
                           :ref:`anchor position <ref.anchors>`.
        :returns: This internal_image.
        """
        if size is None:
            rect = Rect(position)
        else:
            rect = Rect(position, size)
        offset = self._calculate_offset(anchor, rect.size)
        pygame.draw.arc(self._surf, color, (rect.pos + offset, rect.size),
                        start_angle, end_angle, border_width)
        self._version += 1
        scale_surface.clear(self._surf)
        return self

    def draw_internal_image(self, internal_image, position=(0, 0), anchor='topleft'):
        """
        Draws another internal_image over this one.

        :param internal_image: The internal_image to overlay on top of this one.
        :type internal_image: :class:`InternalImage <designer.core.internal_image.InternalImage>`
        :param position: The position of this internal_image.
        :type position: :class:`Vec2D <spyral.Vec2D>`
        :param str anchor: The anchor parameter is an
                           :ref:`anchor position <ref.anchors>`.
        :returns: This internal_image.
        """
        offset = self._calculate_offset(anchor, internal_image._surf.get_size())
        self._surf.blit(internal_image._surf, position + offset)
        self._version += 1
        scale_surface.clear(self._surf)
        return self

    def draw_surface(self, surf, position=(0, 0), anchor='topleft'):
        """
        Draws a pygame surface over this one.

        :param internal_image: The internal_image to overlay on top of this one.
        :type internal_image: :class:`InternalImage <designer.core.internal_image.InternalImage>`
        :param position: The position of this internal_image.
        :type position: :class:`Vec2D <spyral.Vec2D>`
        :param str anchor: The anchor parameter is an
                           :ref:`anchor position <ref.anchors>`.
        :returns: This internal_image.
        """
        offset = self._calculate_offset(anchor, surf.get_size())
        self._surf.blit(surf, position + offset)
        self._version += 1
        scale_surface.clear(self._surf)
        return self

    def rotate(self, angle):
        """
        Rotates the internal_image by angle degrees clockwise. This may change the internal_image
        dimensions if the angle is not a multiple of 90.

        Successive rotations degrate internal_image quality. Save a copy of the
        original if you plan to do many rotations.

        :param float angle: The number of degrees to rotate.
        :returns: This internal_image.
        """
        self._surf = pygame.transform.rotate(self._surf, angle).convert_alpha()
        self._version += 1
        return self

    def scale(self, size):
        """
        Scales the internal_image to the destination size.

        :param size: The new size of the internal_image.
        :type size: :class:`Vec2D <spyral.Vec2D>`
        :returns: This internal_image.
        """
        self._surf = pygame.transform.smoothscale(self._surf,
                                                  size).convert_alpha()
        self._version += 1
        return self

    def flip(self, flip_x=True, flip_y=True):
        """
        Flips the internal_image horizontally, vertically, or both.

        :param bool flip_x: whether to flip horizontally.
        :param bool flip_y: whether to flip vertically.
        :returns: This internal_image.
        """
        self._version += 1
        self._surf = pygame.transform.flip(self._surf,
                                           flip_x, flip_y).convert_alpha()
        return self

    @classmethod
    def from_surface(cls, surf: pygame.Surface):
        image = InternalImage(size=surf.get_size())
        return image.draw_surface(surf)

    def copy(self):
        """
        Returns a copy of this internal_image that can be changed while preserving the
        original.

        :returns: A new internal_image.
        """
        new = copy.copy(self)
        new._surf = self._surf.copy()
        return new

    def crop(self, position, size=None):
        """
        Removes the edges of an internal_image, keeping the internal rectangle specified
        by position and size.

        :param position: The upperleft corner of the internal rectangle that
                         will be preserved.
        :type position: a :class:`Vec2D <spyral.Vec2D>` or a
                        :class:`Rect <spyral.Rect>`.
        :param size: The size of the internal rectangle to preserve. If a Rect
                     was passed in for position, this should be None.
        :type size: :class:`Vec2D <spyral.Vec2D>` or None.
        :returns: This internal_image.
        """
        if size is None:
            rect = Rect(position)
        else:
            rect = Rect(position, size)
        new = DesignerSurface(size)
        new.blit(self._surf, (0, 0), (rect.pos, rect.size))
        self._surf = new
        self._version += 1
        return self

    def _calculate_offset(self, anchor_type, size=(0, 0)):
        """
        Internal method for calculating the offset associated with an
        anchor type.

        :param anchor_type: A string indicating the position of the anchor,
                            taken from :ref:`anchor position <ref.anchors>`. A
                            numerical offset can also be specified.
        :type anchor_type: str or a :class:`Vec2D <spyral.Vec2D>`.
        :param size: The size of the region to offset in.
        :type size: :class:`Vec2D <spyral.Vec2D>`.
        """
        w, h = self._surf.get_size()
        w2, h2 = size

        if anchor_type == 'topleft':
            return Vec2D(0, 0)
        elif anchor_type == 'topright':
            return Vec2D(w - w2, 0)
        elif anchor_type == 'midtop':
            return Vec2D((w - w2) / 2., 0)
        elif anchor_type == 'bottomleft':
            return Vec2D(0, h - h2)
        elif anchor_type == 'bottomright':
            return Vec2D(w - w2, h - h2)
        elif anchor_type == 'midbottom':
            return Vec2D((w - w2) / 2., h - h2)
        elif anchor_type == 'midleft':
            return Vec2D(0, (h - h2) / 2.)
        elif anchor_type == 'midright':
            return Vec2D(w - w2, (h - h2) / 2.)
        elif anchor_type == 'center':
            return Vec2D((w - w2) / 2., (h - h2) / 2.)
        else:
            return Vec2D(anchor_type) - Vec2D(w2, h2)
