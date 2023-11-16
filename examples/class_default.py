from dataclasses import dataclass
from designer import *

@dataclass
class World:
    label: DesignerObject = text("black", "Hello World!", 30)

when('starting', World)
start()

