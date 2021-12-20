from designer import *

diamond = shape('blue',
                30, 0,
                0, -30,
                -30, 0,
                0, 30)

star = shape('red',
             # Starting from inner right point
             (5, 0), (10, -5), (4, -5), (0, -12),  # to top tip
             (-4, -5), (-10, -5), (-5, 0),  # to the inner left point
             (-7, 10), (0, 5), (7, 10)
)

pinhole = circle('black', 2)

spin(star, 10)

draw(pinhole, diamond, star)
