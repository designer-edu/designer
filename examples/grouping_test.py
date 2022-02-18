from designer import *

box = rectangle('black', 50, 130)
top_circle = change_y(circle('red', 15), -45)
middle_circle = circle('yellow', 15)
bottom_circle = change_y(circle('green', 15), 45)
traffic_light = group(box, top_circle, middle_circle, bottom_circle)

move_to_xy(traffic_light, 130, 130)

start(traffic_light)

#start(top_circle, middle_circle, bottom_circle, box)