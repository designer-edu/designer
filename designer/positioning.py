import pygame

from designer.objects.designer_object import DesignerObject
from designer.objects.group import group


def above(top: DesignerObject, bottom: DesignerObject):
    """ Moves the bottom to be below the top """
    bottom.x = top.x + top.width/2 - bottom.width/2
    bottom.y = top.y + top.height
    return group(top, bottom)


def below(bottom: DesignerObject, top: DesignerObject):
    """ Moves the bottom to be below the top """
    bottom.x = top.x + abs(top.width - bottom.width)//2
    bottom.y = top.y + top.height
    return group(top, bottom)


def beside(left: DesignerObject, right: DesignerObject):
    """
    Moves the two objects so that they are both centered on each other's side.
    There will be equal space on either side.
    Vertically, their new y coordinate will be the average of their old positions.
    """
    offset_x = (left.width + right.width)//2
    left.x = left.x - offset_x
    right.x = right.x + offset_x
    vertical_y = (left.y + right.y)//2
    left.y, right.y = vertical_y, vertical_y
    return group(left, right)
