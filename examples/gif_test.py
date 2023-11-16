from designer import *
from dataclasses import dataclass


@dataclass
class World():
    corgi: DesignerObject


def create_world():
    return World(image('https://media.tenor.com/G0JAlvNb_ucAAAAd/corgi-excited.gif'))


when('starting', create_world)
start()