import pygame
import math

from designer.utilities.vector import Vec2D
from designer.utilities.rect import Rect


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
    new = Image(size=(width, height))
    for image, (x, y) in sequence:
        new.draw_image(image, (x, y))
    return new