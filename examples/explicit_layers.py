from designer import *
from dataclasses import dataclass

@dataclass
class World:
    box: DesignerObject
    label: DesignerObject
    box2: DesignerObject
    label2: DesignerObject
    green_circle: DesignerObject
    orange_circle: DesignerObject

set_window_layers(['background', 'foreground'])


@starting
def create_world() -> World:
    box = rectangle('pink', 20, 50)
    label = text('black', "Background Box", 20)
    box.size = label.size
    box2 = rectangle('cornflowerblue', 50, 20)
    label2 = text('black', "Foreground Box", 20)
    box2.size = label2.size
    box.layer = 'background'
    label.layer = 'background:above'
    box2.layer = 'foreground'
    label2.layer = 'foreground:above'
    # Make circle in background layer appear behind everything else
    green_circle = circle('green', 200, 200)
    green_circle.layer = 'background:bottom'
    orange_circle = circle('orange', 5)
    orange_circle.layer = 'foreground:top'

    linear_animation(box2, 'x', 0, get_width(), 3, loop=True)
    linear_animation(label2, 'x', 0, get_width(), 3, loop=True)

    linear_animation(box, 'y', 0, get_height(), 3, loop=True)
    linear_animation(label, 'y', 0, get_height(), 3, loop=True)

    return World(box, label, box2, label2, green_circle, orange_circle)

start()