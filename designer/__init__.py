from os import environ

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

# For `debug` support on Mac, we need to preload tkinter
from designer.system import setup_debug_mode
setup_debug_mode()

# Actually import all dependencies
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
from designer.movement import *

GLOBAL_DIRECTOR: Director = None

__all__ = [
    'circle', 'ellipse',
    'arc', 'line',
    'rectangle',
    'text',
    'shape', 'lines', 'pen',
    'background_image',
    'image', 'emoji',
    'group',
    'draw',
    # Window information
    'set_window_color', 'get_window_color',
    'set_window_size',
    'get_height', 'get_window_height',
    'get_width', 'get_window_width',
    # Events
    'when', 'starting', 'updating', 'typing', 'clicking',
    'start', 'debug',
    'stop',
    'pause',
    'colliding', 'colliding_with_mouse',
    'destroy',
    'DesignerObject',
    # Positioning
    'above', 'below',
    # Director stuff
    'get_director',
    # Window stuff
    'set_window_title', 'get_window_title', 'set_window_image',
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
    'get_music_volume', 'stop_music', 'rewind_music', 'continue_music', 'set_music_position', 'get_music_position',
    # Movement
    'move_forward', 'move_backward', 'turn_left', 'turn_right', 'go_to', 'go_to_xy', 'go_to_mouse',
    'point_towards', 'point_towards_mouse', 'point_in_direction', 'change_xy', 'change_x', 'change_y', 'set_x', 'set_y',
    'get_angle', 'get_x', 'get_y',
    'flip_x', 'flip_y', 'set_flip_x', 'set_flip_y', 'set_scale', 'set_scale_x', 'set_scale_y', 'set_background_image',
    'get_scale', 'get_scale_x', 'get_scale_y', 'get_visible', 'get_flip_x', 'get_flip_y', 'show', 'hide',
    'grow', 'grow_x', 'grow_y', 'shrink',
    'move_to_x', 'move_to_y', 'move_to', 'move_to_mouse', 'move_to_xy',
    'set_visible', 'change_scale',
    # Emoji specific
    'get_emoji_name', 'set_emoji_name'
]
