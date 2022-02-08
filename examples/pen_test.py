from designer import *
from random import randint

turtle = pen()

set_window_title(None)

#turtle.move_to(100, 100)
#turtle.move_to(500, 100)
#turtle.move_to(500, 500)
#turtle.move_to(100, 500)

for i in range(100):
    turtle.move_to(randint(0, get_width()), randint(0, get_height()))

start(turtle)