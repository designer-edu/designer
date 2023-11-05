from designer import *
from dataclasses import dataclass
from random import randint


@dataclass
class PlayerSettings:
    avatar: str
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
    circles: list[DesignerObject]
    counter: int
    cursor: DesignerObject
    available_emoji: list[DesignerObject]
    chosen_index: int


@dataclass
class Overworld:
    player: DesignerObject
    score: DesignerObject
    lives: DesignerObject
    settings: PlayerSettings
    pause_button: Button


@dataclass
class PauseScreen:
    header: DesignerObject
    settings: PlayerSettings
    resume_button: Button
    cursor: DesignerObject
    available_emoji: list[DesignerObject]
    chosen_index: int


def create_overworld(chosen_index: int) -> Overworld:
    avatar = ["dog", "cat", "mouse"][chosen_index]
    return Overworld(emoji(avatar),
                     text("black", "Score: 0", 20, get_width()/2, get_height()/4),
                     text("black", "Lives: 3", 20, get_width()/2, get_height()/4 + 40),
                     PlayerSettings(avatar, 0, 3),
                     make_button("Pause", 200, 200))

def handle_overworld_buttons(world: Overworld):
    if colliding_with_mouse(world.pause_button.background):
        push_scene('pause', settings=world.settings)


def create_pause_screen(settings: PlayerSettings) -> PauseScreen:
    starting_index = ["dog", "cat", "mouse"].index(settings.avatar)
    emoji_list = [
        emoji("dog", get_width() / 3, 200),
        emoji("cat", get_width() / 2, 200),
        emoji("mouse", 2 * get_width() / 3, 200)
    ]
    return PauseScreen(text("black", "Pause", 40),
                       settings,
                       make_button("Resume", get_width() / 2, 400),
                       rectangle("black", 32, 32,
                                 emoji_list[starting_index].x, emoji_list[starting_index].y, 1),
                       emoji_list,
                       starting_index)


def create_title_screen() -> TitleScreen:
    return TitleScreen(text("black", "Title", 40),
                       make_button("Begin Game", get_width() / 2, 400),
                       make_button("Quit to desktop", get_width() / 2, 500))


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
                       [], 0,
                       rectangle("black", 32, 32,
                                 emoji_list[starting_index].x, emoji_list[starting_index].y, 1),
                       emoji_list,
                       starting_index
    )


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


def handle_pause_screen_buttons(world: PauseScreen):
    if colliding_with_mouse(world.resume_button.background):
        pop_scene(chosen_index=world.chosen_index)
    for i, emoji in enumerate(world.available_emoji):
        if colliding_with_mouse(emoji):
            world.chosen_index = i
            world.cursor.x = emoji.x
            world.cursor.y = emoji.y
            world.settings.avatar = ["dog", "cat", "mouse"][i]

def make_balls(world):
    world.counter += 1
    world.circles.append(text("red", str(world.counter), 32, randint(0, get_width()), randint(0, get_height())))
    if len(world.circles) > 30:
        destroy(world.circles.pop(0))

def count_sprites(world):
    print(len(get_director().all_sprites))
    print(len({sprite._scene() for sprite in get_director().all_sprites}))

def resume_from_pause(world: Overworld, chosen_index: int):
    world.settings.avatar = ["dog", "cat", "mouse"][chosen_index]
    world.player.name = world.settings.avatar

when('starting: title', create_title_screen)
when('clicking: title', handle_title_buttons)
when('starting: setup', create_setup_screen)
when('clicking: setup', handle_setup_buttons)
when('updating: setup', make_balls)
when('clicking: title', count_sprites)
when('clicking: setup', count_sprites)
when('starting: overworld', create_overworld)
when('clicking: overworld', handle_overworld_buttons)
when('starting: pause', create_pause_screen)
when('clicking: pause', handle_pause_screen_buttons)
when('entering: overworld', resume_from_pause)
#when('starting.overworld', create_overworld)
#when('starting.pause', create_pause)
#when('starting.level', create_level)
#when('leaving.pause', copy_settings)

debug(scene='title')
