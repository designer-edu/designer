"""

"""

from designer import *
from dataclasses import dataclass


@dataclass
class Title:
    header: DesignerObject
    start_button: DesignerObject
    quit_button: DesignerObject

    @starting
    @staticmethod
    def start(self):
        """
        Could use encapsulation to have all the methods tied to the class.
        Requires a lot of decorators.
        """
        return Title(text("black", "Title", 40),
                     emoji("button"), emoji("button"))


@dataclass
class GameOver:
    header: DesignerObject
    quit_button: DesignerObject
    restart_button: DesignerObject

@dataclass
class Level1:
    player: DesignerObject
    enemy: DesignerObject


when('updating', )

start()