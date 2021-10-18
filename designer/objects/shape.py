import pygame

import designer
from designer.colors import _process_color
from designer.helpers import get_width, get_height
from designer.objects.designer_object import DesignerObject

class Shape(DesignerObject):
    def __init__(self, points, left, top, width, height, color):

        super().__init__()
        self.dirty = 1
        color = _process_color(color)


        self.image = pygame.surface.Surface((width, height), pygame.SRCALPHA, 32).convert_alpha()
        pygame.draw.polygon(self.image, color, points)

        self.rect = self.image.get_rect()
        self.rect.topleft = (left, top)

        super().add()


def shape(color, points):
    '''
   Function to create a shape of at least three points.

   :param color: color of shape.
   :type color: str
   :param points: coordinates of points of shape
   :type points: List[Tuple] in (x, y), (x, y) format of points to be connected of shape
   :return: Shape object created
   '''
    designer.check_initialized()
    max_x = 0
    max_y = 0
    new_points = []
    min_x = designer.GLOBAL_DIRECTOR.width
    min_y = designer.GLOBAL_DIRECTOR.height
    for pt in points:
        if pt[0] < min_x:
            min_x = pt[0]
        if pt[0] > max_x:
            max_x = pt[0]
        if pt[1] < min_y:
            min_y = pt[1]
        if pt[1] > max_y:
            max_y = pt[1]
        x = designer.GLOBAL_DIRECTOR.width - pt[0]
        y = designer.GLOBAL_DIRECTOR.height - pt[1]
        new_points.append((x, y))
    width = max_x - min_x
    height = max_y - min_y
    new_points = [(x - min_x, y - min_y) for x, y in points]
    return Shape(new_points, min_x, min_y, width, height, color)