import pygame

from designer.objects.designer_object import DesignerObject
from designer.objects.group import group


def above(top: DesignerObject, bottom: DesignerObject):
    """ Moves the bottom to be below the top """
    bottom.x = top.x + top.width/2 - bottom.width/2
    bottom.y = top.y + top.height
    return group(top, bottom)

def below(bottom: DesignerObject, top: DesignerObject, ):
    """ Moves the bottom to be below the top """
    bottom.x = top.x + abs(top.width - bottom.width)//2
    bottom.y = top.y + top.height
    return group(top, bottom)
