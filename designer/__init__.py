import pygame
from designer.Director import *
from designer.Animation import *
from designer.DesignerObject import *
from designer.colors import *

GLOBAL_DIRECTOR = None

__all__ = [
    'circle',
    'ellipse',
    'arc',
    'line',
    'rectangle',
    'text',
    'shape',
    'image',
    'group',
    'draw',
    'set_window_color',
    'set_window_size',
    'glide_around',
    'glide_right',
    'glide_left',
    'glide_up',
    'glide_down',
    'glide_in_degrees',
    'rotate'
]
