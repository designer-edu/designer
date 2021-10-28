from os import environ

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame
from designer.core.director import *
from designer.core.event import *
from designer.helpers import *
from designer.animation import *
from designer.objects import *
from designer.colors import *

GLOBAL_DIRECTOR: Director = None

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
    'rotate',
    'get_height',
    'get_width',
    'when',
    'colliding',
    'destroy',
    'DesignerObject'
]
