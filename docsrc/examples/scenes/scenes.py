from designer import *
from dataclasses import dataclass
from random import randint


@dataclass
class Button:
    """
    A Button is a collection of designer objects that are grouped together to form a button.
    The background and border are just rectangles, while the label is a text object.
    """
    background: DesignerObject
    border: DesignerObject
    label: DesignerObject


def make_button(message: str, x: int, y: int) -> Button:
    horizontal_padding = 4
    vertical_padding = 2
    label = text("black", message, 20, x, y, layer='top')
    return Button(rectangle("cyan", label.width + horizontal_padding, label.height + vertical_padding, x, y),
                  rectangle("black", label.width + horizontal_padding, label.height + vertical_padding, x, y, 1),
                  label)


@dataclass
class PlayerSettings:
    """
    Shared dataclass that can be transmitted across scenes. Note that it doesn't have any designer objects,
    since those cannot be sent across states!
    """
    avatar: str
    score: int
    lives: int


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


PLAYER_AVATARS = ["dog", "cat", "mouse"]


def create_title_screen() -> TitleScreen:
    """ Title screen is simple, just two buttons and a header """
    return TitleScreen(text("black", "Title", 40),
                       make_button("Begin Game", get_width() / 2, 400),
                       make_button("Quit to desktop", get_width() / 2, 500))


def create_setup_screen() -> SetupScreen:
    """ Setup screen has two buttons (start/back), but also three emoji that you can click
    on to choose your avatar. There's a black box overlaid on top of the emoji. """
    starting_index = 0
    emoji_list = [
        emoji(avatar, ((2 + i) * get_width()) / 5, 200)
        for i, avatar in enumerate(PLAYER_AVATARS)
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


def create_overworld(chosen_index: int) -> Overworld:
    """ The overworld is mostly just the player character and the pause button.
    But wait! That parameter there comes from a PREVIOUS SCENE! Or the pause screen.
    Anything that creates the overworld needs to be sure to pass in
    the chosen_index of the player, since that will be used to update the overworld."""
    avatar = PLAYER_AVATARS[chosen_index]
    return Overworld(emoji(avatar),
                     text("black", "Score: 0", 20, get_width()/2, get_height()/4),
                     text("black", "Lives: 3", 20, get_width()/2, get_height()/4 + 40),
                     PlayerSettings(avatar, 0, 3),
                     make_button("Pause", 200, 200))

def create_pause_screen(settings: PlayerSettings) -> PauseScreen:
    """
    The pause screen is similar to the setup screen, but it has a resume button instead of a start button.
    The settings also come in from the overworld, so we can reflect the currently chosen character.
    Note that the settings CAN be modified from the pause menu, or you can pass parameters back when you
    pop the scene later.
    """
    starting_index = PLAYER_AVATARS.index(settings.avatar)
    emoji_list = [
        emoji(avatar, ((2+i) * get_width()) / 5, 200)
        for i, avatar in enumerate(PLAYER_AVATARS)
    ]
    return PauseScreen(text("black", "Pause", 40),
                       settings,
                       make_button("Resume", get_width() / 2, 400),
                       rectangle("black", 32, 32,
                                 emoji_list[starting_index].x, emoji_list[starting_index].y, 1),
                       emoji_list,
                       starting_index)

def handle_title_buttons(world: TitleScreen):
    """
    Buttons are pretty easy, just use the `clicking` event with the `colliding_with_mouse` function.

    The change_scene(scene_name) function can be used to change scenes. This will call the relevant
    `"starting: scene_name"` function and create the new scene.
    """
    if colliding_with_mouse(world.start_button.background):
        change_scene('setup')
    if colliding_with_mouse(world.quit_button.background):
        quit()


def handle_setup_buttons(world: SetupScreen):
    """
    The change_scene(scene_name) function can also take any number of KEYWORD arguments. That means
    you provide the name of the parameter and the argument itself. That parameter will be passed into
    the corresponding `"starting: scene_name"` function as a parameter with the same name.

    We also have some logic here to handle choosing a new avatar
    """
    if colliding_with_mouse(world.start_button.background):
        change_scene('overworld', chosen_index=world.chosen_index)
    if colliding_with_mouse(world.back_button.background):
        change_scene('title')

    # Handle picking a new avatar
    for i, emoji in enumerate(world.available_emoji):
        if colliding_with_mouse(emoji):
            world.chosen_index = i
            world.cursor.x = emoji.x
            world.cursor.y = emoji.y


def handle_overworld_buttons(world: Overworld):
    """
    The push_scene(scene_name) function can be used to push a new scene onto the stack. Unlike change_scene,
    this will not destroy the current scene, but instead will pause it. When the new scene is popped, the old
    scene will be resumed. In this case, we push the pause screen onto the stack, and pass in the current
    settings as a parameter. Then, when the pause screen is popped, we can resume the overworld with the
    updated settings.
    """
    if colliding_with_mouse(world.pause_button.background):
        push_scene('pause', settings=world.settings)


def handle_pause_screen_buttons(world: PauseScreen):
    """
    The pop_scene() function can be used to pop the current scene off the stack. This will destroy the current
    scene, and resume the previous scene. In this case, we pop the pause screen off the stack, and pass in the
    chosen_index as a parameter. Then, when the overworld is resumed, we can update the player's avatar.
    Technically, we don't have to pass in the chosen_index, since the settings are already passed in, but
    it's good practice to pass in any parameters that you want to use in the next scene.
    """
    if colliding_with_mouse(world.resume_button.background):
        pop_scene(chosen_index=world.chosen_index)
    for i, emoji in enumerate(world.available_emoji):
        if colliding_with_mouse(emoji):
            world.chosen_index = i
            world.cursor.x = emoji.x
            world.cursor.y = emoji.y
            world.settings.avatar = PLAYER_AVATARS[i]

def resume_from_pause(world: Overworld, chosen_index: int):
    """
    This function is called when the overworld is resumed from the pause screen. We can use this to update
    the player's avatar.
    """
    world.settings.avatar = PLAYER_AVATARS[chosen_index]
    # This actually changes the current emoji to the new picture
    world.player.name = world.settings.avatar

"""
The when function is used to register events. The first parameter is the event name, and the second parameter
is the function that will be called when that event is triggered. The event name here has a special format
with a colon in it. This is used to specify which scene the event is for. In this case, we have four scenes:
title, setup, overworld, and pause. Each scene has its own set of events. This is useful because it means
that you can have distinct events for each scene.
"""
when('starting: title', create_title_screen)
when('clicking: title', handle_title_buttons)
when('starting: setup', create_setup_screen)
when('clicking: setup', handle_setup_buttons)
when('starting: overworld', create_overworld)
when('clicking: overworld', handle_overworld_buttons)
when('starting: pause', create_pause_screen)
when('clicking: pause', handle_pause_screen_buttons)
when('entering: overworld', resume_from_pause)

"""
The debug function is used to start the game. It takes an optional parameter, which is the name of the
starting scene. If no scene is provided, it will start with the first scene that was registered.
The debug function works exactly the same as the start function, except that it will also open a window
that shows the current game state.
"""
debug(scene='title')
