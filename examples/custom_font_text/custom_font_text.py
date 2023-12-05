from designer import *
from dataclasses import dataclass


@dataclass
class World:
    title: DesignerObject
    pangram: DesignerObject


def create_world() -> World:
    world = World(
        text(
            'black', "Some Sample Text", 30,
            font_name="RubikBubbles", font_path="RubikBubbles-Regular.ttf"
        ),
        text(
            'black', "The quick brown fox jumps over the lazy dog.",
            30, font_name="RubikBubbles"
        )
    )
    world.title.y -= 20
    world.pangram.y += 20
    return world


when('starting', create_world)
start()
