import pygame

import math

from designer.colors import _process_color
from designer.helpers import get_width, get_height
from designer.objects.designer_object import DesignerObject

class Line(DesignerObject):
    def __init__(self, start, end, thickness, color):
        """
        Creates Line Designer Object on window.

        :param start: starting coordinates of line
        :type start: Tuple[int]
        :param end: ending coordinates of line
        :type end: Tuple[int]
        :param thickness: thickness of line in pixels
        :type thickness: int
        :param color: color of line
        :type color: str or List[str]
        """

        super().__init__()
        color = _process_color(color)
        self.dirty = 1

        (x1, y1), (x2, y2) = start, end
        # Need to flip y-axis
        angle = math.atan2(-(y2 - y1), x2 - x1) % 2 * math.pi
        p1x, p1y = x1 + math.cos(angle + math.pi / 2) * thickness, y1 + math.sin(angle + math.pi / 2) * thickness
        p2x, p2y = x1 + math.cos(angle - math.pi / 2) * thickness, y1 - math.sin(angle + math.pi / 2) * thickness
        p3x, p3y = x2 + math.cos(angle + math.pi / 2) * thickness, y2 + math.sin(angle + math.pi / 2) * thickness
        p4x, p4y = x2 + math.cos(angle - math.pi / 2) * thickness, y2 - math.sin(angle + math.pi / 2) * thickness
        left = min(p1x, p2x, p3x, p4x)
        right = max(p1x, p2x, p3x, p4x)
        top = min(p1y, p2y, p3y, p4y)
        bottom = max(p1y, p2y, p3y, p4y)

        # calculate differences between x and y coordinates of line
        x = abs(start[0] - end[0])
        y = abs(start[1] - end[1])

        width = right - left
        height = bottom - top

        new_start = (x1 - left), (y1 - top)
        new_end = (x2 - left), (y2 - top)

        # create a surface of the width and height of the line
        self.image = pygame.surface.Surface((width, height), pygame.SRCALPHA, 32).convert_alpha()
        pygame.draw.line(self.image, color, new_start, new_end, thickness)
        self.rect = pygame.Rect(left, top, width, height)

        # set top left corner of rect to minimum of x and y points of line (this should guarantee top left coordinates)
        self.rect.left = left
        self.rect.top = top
        super().add()


def line(color, thickness, *args):
    '''
    Function to create a line.

    :param thickness: thickness of line in pixels
    :type thickness: int
    :param color: color of line
    :type color: str or List[str]
    :param args: start and end coordinates of line
    :type args: two tuples (start x, start y), (end x, end y) or four ints start x, start y, end x, end y

    :return: Line object created
    '''
    if len(args) > 2:
        start = args[0], args[1]
        end = args[2], args[3]
    else:
        start = args[0]
        end = args[1]
    return Line(start, end, thickness, color)