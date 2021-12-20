from os import environ

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame
from designer.core.director import *
from designer.core.event import *
from designer.helpers import *
from designer.animation import *
from designer.utilities.easings import *
from designer.objects import *
from designer.colors import *
from designer.positioning import *
from designer.keyboard import *
from designer.mouse import *

GLOBAL_DIRECTOR: Director = None

__all__ = [
    'circle', 'ellipse',
    'arc', 'line',
    'rectangle',
    'text',
    'shape', 'lines',
    'background_image',
    'image',
    'group',
    'draw',
    'set_window_color',
    'set_window_size',
    'get_height',
    'get_width',
    'when',
    'start',
    'stop',
    'pause',
    'colliding',
    'destroy',
    'DesignerObject',
    'above', 'below',
    # Director stuff
    'get_director',
    # Window stuff
    'set_window_title', 'get_window_title',
    # Keyboard stuff
    'get_keyboard_repeat', 'set_keyboard_repeat',
    'get_keyboard_delay', 'set_keyboard_delay',
    'get_keyboard_interval', 'set_keyboard_interval',
    'enable_keyboard_repeating', 'disable_keyboard_repeating',
    # Mouse stuff
    'get_mouse_cursor', 'set_mouse_cursor',
    'get_mouse_visible', 'set_mouse_visible',
    'get_mouse_position', 'set_mouse_position',
    'get_mouse_x', 'get_mouse_y',
    # Animations
    'Animation', 'linear_animation', 'sequence_animation',
    'glide_around',
    'glide_right',
    'glide_left',
    'glide_up',
    'glide_down',
    'glide_in_degrees',
    'spin',
    # Easings
    'Linear', 'Iterate',
    # Music
    'play_sound',
    'play_music', 'background_music', 'pause_music', 'set_music_volume', 'is_music_playing',
    'get_music_volume', 'stop_music', 'rewind_music', 'continue_music', 'set_music_position', 'get_music_position'
]
