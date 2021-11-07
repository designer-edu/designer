from designer import *
green_rect = rectangle('green', 50, 50)
blue_rect = rectangle('blue', 100, 100)

# Because we don't pass in blue_rect, it won't be visible!
draw(green_rect)
