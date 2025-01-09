from dataclasses import dataclass
from designer import *
from math import atan2, degrees, radians

@dataclass
class World:
    angle_text: DesignerObject
    distance_text: DesignerObject
    angle_line: DesignerObject


def create_world() -> World:
    """ Create the world """
    angle_text = text("black", "Angle: 0", 40, get_width()/2, get_height()/3)
    distance_text = text("black", "Distance: 0", 40, get_width()/2, 2*get_height()/3)
    angle_line = line("black", get_width()/2, get_height()/2, 1, 1)
    return World(angle_text, distance_text, angle_line)


def update_angle(world: World):
    mouse_pos = get_mouse_position()
    angle = degrees(atan2(-mouse_pos[1] + get_height()/2, mouse_pos[0] - get_width()/2)) % 360
    world.angle_text.text = f"Angle: {angle}"
    if mouse_pos[0] and mouse_pos[1]:
        world.angle_line.start_x, world.angle_line.start_y = get_width()/2, get_height()/2
        world.angle_line.end_y, world.angle_line.end_x = mouse_pos


when('starting', create_world)
when('updating', update_angle)

start()