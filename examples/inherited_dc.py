from designer import *
import math


class SpeedEmoji(emoji):
    speed: int


@updating
def update_emoji(se: SpeedEmoji):
    se.speed = (se.speed+10) % 360
    se.x += math.sin(math.radians(se.speed))*10


start(SpeedEmoji("dog", speed=5))
