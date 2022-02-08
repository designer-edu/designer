from designer import *
from random import randint

pinhole = circle('black', 3)

dragon = emoji("😻")
dragon2 = emoji("🦖")
dragon2['x'] += 200
dragon2['angle'] += 45
dragon2['scale'] = 2

dragon3 = emoji("🐉")
dragon3['x'] += 272
dragon3['angle'] -= 45
dragon3['scale'] = 2
dragon3['flip_x'] = True

dog = emoji("dog")
dog['x'] -= 300
spin(dog)

pinhole2 = circle('black', 3)
pinhole2['x'] += 200
pinhole3 = circle('black', 3)
pinhole3['x'] -= 300
spin(pinhole3)

others = [emoji(character, x=randint(18, get_width()-18), y=randint(18, get_height()-18))
          for character in "👻❤🚀⌛☕⚡⛄⭐🌻🚐"]

draw(dragon, dragon2, dragon3, dog, pinhole, pinhole2, pinhole3, others)