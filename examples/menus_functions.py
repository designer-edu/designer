from designer import *
from dataclasses import dataclass


@dataclass
class PlayerSettings:
    current_color: str
    score: int
    lives: int


@dataclass
class Button:
    background: DesignerObject
    border: DesignerObject
    label: DesignerObject


def make_button(message: str, x: int, y: int) -> Button:
    label = text("black", message, 20, x, y, layer='top')
    return Button(rectangle("cyan", label.width + 4, label.height + 2, x, y),
                  rectangle("black", label.width + 4, label.height + 2, x, y, 1),
                  label)


@dataclass
class TitleScreen:
    header: DesignerObject
    start_button: Button
    quit_button: Button


@dataclass
class SetupScreen:
    header: DesignerObject
    start_button: Button
    back_button: Button
    cursor: DesignerObject
    available_emoji: list[DesignerObject]
    chosen_index: int


def create_title_screen() -> TitleScreen:
    return TitleScreen(text("black", "Title", 40),
                       make_button("Start", get_width() / 2, 400),
                       make_button("Quit", get_width() / 2, 500))


def create_setup_screen() -> SetupScreen:
    starting_index = 0
    emoji_list = [
        emoji("dog", get_width() / 3, 200),
        emoji("cat", get_width() / 2, 200),
        emoji("mouse", 2 * get_width() / 3, 200)
    ]
    return SetupScreen(text("black", "Setup", 40),
                       make_button("Start", get_width() / 2, 400),
                       make_button("Back", get_width() / 2, 500),
                       rectangle("black", 32, 32,
                                 emoji_list[starting_index].x, emoji_list[starting_index].y, 1),
                       emoji_list,
                       starting_index)


def handle_title_buttons(world: TitleScreen):
    if colliding_with_mouse(world.start_button.background):
        change_scene('setup')
    if colliding_with_mouse(world.quit_button.background):
        quit()


def handle_setup_buttons(world: SetupScreen):
    if colliding_with_mouse(world.start_button.background):
        change_scene('overworld', chosen_index=world.chosen_index)
    if colliding_with_mouse(world.back_button.background):
        change_scene('title')
    for i, emoji in enumerate(world.available_emoji):
        if colliding_with_mouse(emoji):
            world.chosen_index = i
            world.cursor.x = emoji.x
            world.cursor.y = emoji.y

"""
        change_window('overworld', chosen_index=world.chosen_index)

        push_window('pause', )
        pop_window()

        change_window('level', level_id=1)
        change_window('level', level_id=2)
        
        change_window('home')
        change_window('neighbors')
"""

when('starting: title', create_title_screen)
when('clicking: title', handle_title_buttons)
when('starting: setup', create_setup_screen)
when('clicking: setup', handle_setup_buttons)
#when('starting.overworld', create_overworld)
#when('starting.pause', create_pause)
#when('starting.level', create_level)
#when('leaving.pause', copy_settings)

debug(scene='title')
