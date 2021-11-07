from designer import *


def spin(world):
    world['box']['angle'] += 1


when('updating', spin)
start({"box": rectangle("orange", 30, 30)})
