from dataclasses import dataclass
from designer import *
from random import randint
from random import choice

PLAYER_SPEED = 10

class MovingEmoji(Emoji):
    '''
    This is the type that the players are as it has a set speed that gravity will affect
    Attributes:
        speed(int): the speed the players y coordinate will move at
        direction(int): the direction the players are moving
    '''
    speed: int
    direction: int
@dataclass
class Level1:
    '''
    This is the first level of the game
    Attributes:
        ground(DesignerObject): the rectangle representing the ground at the bottom of the level
        cave_entrance_1(DesignerObject): the circle at top of the level that the players will want to reach
        platforms_L1(List[DesignerObject]): list of rectangles to serve as platforms for players to land on
        beat_L1(bool): whether or not the first level was completed
        player_1(MovingEmoji): the first player
        player_2(MovingEmoji): the second player
        player_1_health(int): how much health the first player has
        player_2_health(int): how much health the second player has
        healths(List[DesignerObject]): the health status section at top right displaying 2 healths, 1 for each player
        grounded_1(bool): whether or not player 1 is on the ground
        grounded_2(bool): whether or not player 2 is on the ground
        player_1_left(bool): whether or not the user is making player 1 move left
        player_2_left(bool): whether or not the user is making player 2 move left
        player_1_right(bool): whether or not the user is making player 1 move right
        player_2_right(bool): whether or not the user is making player 2 move right
        player_1_direction(str): the direction player 1 was last moving in
        player_2_direction(str): the direction player 2 was last moving in
        player_1_jump(bool): whether or not the user is making player 1 jump
        player_2_jump(bool): whether or not the user is making player 2 jump
        player_1_speed(int): the speed at which player 1 is moving left or right (positive or negative PLAYER SPEED)
        player_2_speed(int): the speed at which player 1 is moving left or right (positive or negative PLAYER SPEED)
        player_1_flashlight(DesignerObject): the flashlight that will player 1 can control
        player_2_flashlight(DesignerObject): the flashlight that will player 2 can control
        player_1_flash_on(bool): whether or not the user is making player 1's flashlight appear
        player_2_flash_on(bool): whether or not the user is making player 2's flashlight appear
        bats(List[DesignerObject]): the bats that are in the level
    '''
    ground: DesignerObject
    cave_entrance_1: DesignerObject
    platforms_L1: [DesignerObject]
    beat_L1: bool
    player_1: MovingEmoji
    player_2: MovingEmoji
    player_1_health: int
    player_2_health:int
    healths: [DesignerObject]
    grounded_1: bool
    grounded_2: bool
    player_1_left: bool
    player_2_left: bool
    player_1_right: bool
    player_2_right: bool
    player_1_direction:str
    player_2_direction:str
    player_1_jump: bool
    player_2_jump: bool
    player_1_speed: int
    player_2_speed: int
    player_1_flashlight: DesignerObject
    player_2_flashlight: DesignerObject
    player_1_flash_on: bool
    player_2_flash_on: bool
    bats: [DesignerObject]



def create_ground() -> DesignerObject:
    '''
    This creates the ground at bottom of screen
    Return:
        DesignerObject: a rectangle at the bottom of the screen that covers the width of the screen
    '''
    ground = rectangle(color="black",width=get_width()*2,height=40,x=0,y=get_height())
    return ground
def create_cave_entrance_1() -> DesignerObject:
    '''
    This function creates a black circle at the top left of the screen that serves as place for players to go to
    Return:
        DesignerObject: a circle at the top left of the screen with a radius of 50
    '''
    cave_entrance_1 = circle(color="black",radius=50,x=70,y=70)
    return cave_entrance_1

def create_bat() -> DesignerObject:
    '''
    This function creates a bat
    and puts them at a random y coordinate and randomly choosing between the left and right side of the screen
    Returns:
        DesignerObject: emoji of a bat
    :return:
    '''
    bat = emoji("bat")
    bat.x = choice([0,get_width()])
    bat.y = randint(0,get_height())
    return bat
def spawn_bats_1(level1:Level1) -> [DesignerObject]:
    '''
    This function randomly spawns a bat into the level when there are less than 4 bats on the screen
    Args:
        level1(Level1): the level 1 scene in order to check how many bats are on the screen
    Returns:
        List[DesignerObject]: a list of bats that will be on the screen
    '''
    good_num_bats = len(level1.bats) < 4
    if good_num_bats and randint(1,150) == 120:
        level1.bats.append(create_bat())
def move_bats_1(level1:Level1):
    '''
    This function moves the bats toward the players
    Args:
        level1(Level1): the level 1 scene in order to choose which player to make the bat follow and their position
    '''
    for bat in level1.bats:
        target = choice([level1.player_1, level1.player_2])
        point_towards(bat,target)
        target_x = target.x
        target_y = target.y
        if (bat.x > target_x):
            bat.x += -1
        else:
            bat.x += 1
        if (bat.y > target_y):
            bat.y += -1
        else:
            bat.y += 1
def flash_bat_collision_1(level1:Level1):
    '''
    This function checks if a bat collided with a flashlight
    and, if it did, sets it as an argument for the destroy_bats function
    Args:
        level1(Level1): the level 1 scene used to get the flashlight object for the collision check
    '''
    scared_bats = []
    for bat in level1.bats:
        if colliding(bat,level1.player_1_flashlight) and level1.player_1_flash_on:
            scared_bats.append(bat)
        if colliding(bat,level1.player_2_flashlight) and level1.player_2_flash_on:
            scared_bats.append(bat)
    level1.bats = destroy_bats(level1.bats,scared_bats)
def player_bat_collision_1(level1:Level1):
    '''
    This function checks if a bat collided with a player
    and, if it did, sets it as an argument for the destroy_bats function and subtracts 1 hp from the player
    Args:
        level1(Level1): the level 1 scene used to get the player object for the collision check
    '''
    remove_bats = []
    for bat in level1.bats:
        if colliding(bat,level1.player_1):
            level1.player_1_health -= 1
            remove_bats.append(bat)
        if colliding(bat,level1.player_2):
            level1.player_2_health -= 1
            remove_bats.append(bat)
    level1.bats = destroy_bats(level1.bats,remove_bats)
def destroy_bats(scene_bats:[DesignerObject], remove_bats:[DesignerObject]) -> [DesignerObject]:
    '''
    This function removes the specified bats from the level 1 scene and keeps the specified bats on the screen
    Args:
        scene_bats([DesignerObject]): the bats present in the level 1 scene,
        including both the bats we want to keep and the bats we want to remove
        remove_bats([DesignerObject]): the bats present in the level 1 scene that we wish to remove
    Returns:
        List[DesignerObject]: the bats present in the level 1 scene that we want to keep
    '''
    keep_bats = []
    for bat in scene_bats:
        if bat in remove_bats:
            destroy(bat)
        else:
            keep_bats.append(bat)
    return keep_bats
def display_health() -> [DesignerObject]:
    '''
    This function creates a health status section in the top right corner of the screen
    Returns:
        List[DesignerObject]: two lines of white text, one for each player's health
    '''
    healths = [text("white","Player 1 Health: " ,20,(get_width()-100),20),
               text("white","Player 2 Health: ",20,(get_width()-100),40)]
    return healths
def update_health(level1:Level1):
    '''
    This function updates the health that appears in the health status
    Args:
        level1(Level1): the level 1 scene in order to pull each player's current health in level 1
    '''
    for health in level1.healths:
        if health == level1.healths[0]:
            health.text = "Player 1 Health:" + str(level1.player_1_health)
        if health == level1.healths[1]:
            health.text = "Player 2 Health:" + str(level1.player_2_health)
def lost_game(level1:Level1):
    '''
    This function changes the scene to the end screen scene when at least one of the players' hp reaches 0
    Args:
        level1(Level1): the level 1 scene in order to access how much hp each player has
    '''
    if level1.player_1_health == 0 or level1.player_2_health == 0:
        change_scene('endscreen')
def create_plat_L1() -> [DesignerObject]:
    '''
    This function creates 7 rectangles on the screen at different locations
    to serve as platforms for the players to land on
    Returns:
        List[DesignerObject]: a list consisting of multiple rectangles
    '''
    platforms_L1 = [rectangle(color="black", width=80, height=10, x=515, y=get_height() - 80),
                    rectangle(color="black", width=340, height=10, x=290, y=get_height() - 170),
                    rectangle(color="black", width=100, height=10, x=300, y=get_height() - 250),
                    rectangle(color="black", width=50, height=10, x=400, y=get_height() - 320),
                    rectangle(color="black", width=100, height=10, x=370, y=get_height() - 430),
                    rectangle(color="black", width=150, height=10, x=200, y=get_height() - 450),
                    rectangle(color="black", width=200, height=10, x=70, y=120)]
    return platforms_L1
def create_player1() -> MovingEmoji:
    '''
    This creates Player 1 and makes him appear on the bottom left of the screen
    Return:
        MovingEmoji: an emoji to represent the player that has speed of 5 (needed for gravity later) and direction of 0
    '''
    player_1 = MovingEmoji('🧍',speed=5,direction=0)
    grow(player_1, 2)
    player_1.y = get_height()-40
    player_1.x = 120
    return player_1
def create_p1_flashlight() -> DesignerObject:
    '''
    This creates Player 1's flashlight that will appear when the function gets called
    Return:
        DesignerObject: a flashlight emoji that begins as hidden
    '''
    player_1_flashlight = emoji("🔦")
    grow(player_1_flashlight, 1 / 2)
    turn_left(player_1_flashlight, 45)
    player_1_flashlight.flip_x = False
    hide(player_1_flashlight)
    return player_1_flashlight
def move_right_p1(world: Level1):
    '''
    This function moves Player 1 to the right when it gets called
    Args:
        world(Level1): the current scene in order to access player 1's speed and direction
    '''
    world.player_1_speed = PLAYER_SPEED
    world.player_1_direction = "right"
def move_left_p1(world: Level1):
    '''
    This function moves Player 1 to the left when it gets called
    Args:
        world(Level1): the current scene in order to access player 1's speed and direction
    '''
    world.player_1_speed = -PLAYER_SPEED
    world.player_1_direction = "left"
def move_up_p1(world:Level1):
    '''
    This function moves Player 1 up when it gets called to serve as a jump
    Args:
        world(Level1): the current scene in order to access player 1's speed
    '''
    world.player_1.speed += -30
def stop_moving_players(world:Level1):
    '''
    This function prevents Players 1 and 2 from running off of the screen
    Args:
        world(Level1): the current scene in order to access the players' x location
    '''
    if world.player_1.x > get_width():
        world.player_1.x = get_width()
    if world.player_1.x < 0:
        world.player_1.x = 0
    if world.player_2.x > get_width():
        world.player_2.x = get_width()
    if world.player_2.x < 0:
        world.player_2.x = 0
def move_player1(world: Level1):
    '''
    This function takes in the key being pressed and makes Player 1 move accordingly,
    calling the appropriate helper functions
    Args:
        world(Level1): the current scene in order to access player 1's speed, location, and when it's being controlled
    '''
    print("STATUS", world.player_1_flashlight.visible)
    world.player_1.x += world.player_1_speed
    if world.player_1_left:
        move_left_p1(world)
    if world.player_1_right:
        move_right_p1(world)
    if not world.player_1_left and not world.player_1_right:
        world.player_1_speed = 0
    if world.player_1_jump:
        if world.grounded_1:
            move_up_p1(world)
            world.player_1.y += world.player_1.speed
    if world.player_1_flash_on:
       # if world.player_1_direction == "right":
       #     world.player_1_flashlight.y = world.player_1.y + 5
       #     world.player_1_flashlight.x = world.player_1.x + 20
       #     world.player_1_flashlight.flip_x = False
        if world.player_1_direction == "left":
            print("LEFT")
            world.player_1_flashlight.y = world.player_1.y + 5
            world.player_1_flashlight.x = world.player_1.x - 20
            world.player_1_flashlight.flip_x = True
        print("BANANA")
        show(world.player_1_flashlight)
        print("ALPHA")
    if not world.player_1_flash_on:
        print("HERE")
        hide(world.player_1_flashlight)
        print("BETA")
    print("\t", world.player_1_flashlight.visible)
def keys_pressed_p1(world: Level1, key: str):
    '''
    This function checks if the key is still being pressed
    so that Player 1 keeps moving or keeps shining light while the key is being held
    Args:
        world(Level1): the current scene appearing on the screen
        key(str): the key that the user is pressing on their keyboard
    '''
    print(key)
    if key == "A":
        world.player_1_left = True
    if key == "D":
        world.player_1_right = True
    if key == "S":
        world.player_1_flash_on = True
    if key == "W":
        world.player_1_jump = True
def keys_not_pressed_p1(world: Level1, key: str):
    '''
    This function checks if the key has been released
    so that Player 1 stops moving or shining light while the key no longer being held
    Args:
        world(Level1): the current scene appearing on the screen
        key(str): the key that the user is not pressing on their keyboard
    '''
    if key == "A":
        world.player_1_left = False
    if key == "D":
        world.player_1_right = False
    if key == "S":
        world.player_1_flash_on = False
    if key == "W":
        world.player_1_jump = False
def create_player2() -> MovingEmoji:
    '''
    This creates Player 2 and makes him appear on the bottom left of the screen
    Return:
        MovingEmoji: an emoji to represent the player that has speed of 5 (needed for gravity later) and direction of 0
    '''
    player_2 = MovingEmoji('🧍',speed=5,direction=0)
    grow(player_2, 2)
    player_2.y = get_height() - 40
    player_2.x = 20
    return player_2
def create_p2_flashlight() -> DesignerObject:
    '''
    This creates Player 2's flashlight that will appear when the function gets called
    Return:
        DesignerObject: a flashlight emoji that begins as hidden
    '''
    player_2_flashlight = emoji("🔦")
    grow(player_2_flashlight, 1 / 2)
    turn_left(player_2_flashlight, 45)
    hide(player_2_flashlight)
    return player_2_flashlight
def move_right_p2(world: Level1):
    '''
    This function moves Player 2 to the right when it gets called
    Args:
        world(Level1): the current scene in order to access player 2's speed and direction
    '''
    world.player_2_speed = PLAYER_SPEED
    world.player_2_direction = "right"
def move_left_p2(world: Level1):
    '''
    This function moves Player 2 to the left when it gets called
    Args:
        world(Level1): the current scene in order to access player 2's speed and direction
    '''
    world.player_2_speed = -PLAYER_SPEED
    world.player_2_direction = "left"
def move_up_p2(world:Level1):
    '''
    This function moves Player 2 up when it gets called to serve as a jump
    Args:
        world(Level1): the current scene in order to access player 2's speed
    '''
    world.player_2.speed += -30
def move_player2(world: Level1):
    '''
    This function takes in the key being pressed and makes Player 2 move accordingly,
    calling the appropriate helper functions
    Args:
        world(Level1): the current scene in order to access player 2's speed, location, and when it's being controlled
    '''
    world.player_2.x += world.player_2_speed
    if world.player_2_left and world.player_2.x > 0:
        move_left_p2(world)
    if world.player_2_right and world.player_2.x < get_width():
        move_right_p2(world)
    if not world.player_2_left and not world.player_2_right:
        world.player_2_speed = 0
    if world.player_2_jump:
        if world.grounded_2:
            move_up_p2(world)
            world.player_2.y += world.player_2.speed
    if world.player_2_flash_on:
        if world.player_2_direction == "right":
            world.player_2_flashlight.y = world.player_2.y + 5
            world.player_2_flashlight.x = world.player_2.x + 20
        if world.player_2_direction == "left":
            world.player_2_flashlight.y = world.player_2.y + 5
            world.player_2_flashlight.x = world.player_2.x - 20
        show(world.player_2_flashlight)
    if not world.player_2_flash_on:
        hide(world.player_2_flashlight)
def keys_pressed_p2(world: Level1, key: str):
    '''
    This function checks if the key is still being pressed
    so that Player 2 keeps moving or keeps shining light while the key is being held
    Args:
        world(Level1): the current scene appearing on the screen
        key(str): the key that the user is pressing on their keyboard
    '''
    if key == "Left":
        world.player_2_left = True
    if key == "Right":
        world.player_2_right = True
    if key == "Down":
        world.player_2_flash_on = True
    if key == "Up":
        world.player_2_jump = True
def keys_not_pressed_p2(world: Level1, key: str):
    '''
    This function checks if the key has been released
    so that Player 2 stops moving or shining light while the key no longer being held
    Args:
        world(Level1): the current scene appearing on the screen
        key(str): the key that the user is not pressing on their keyboard
    '''
    if key == "Left":
        world.player_2_left = False
    if key == "Right":
        world.player_2_right = False
    if key == "Down":
        world.player_2_flash_on = False
    if key == "Up":
        world.player_2_jump = False
def check_beat_levels(world:Level1):
    '''
    This function checks to see if level 1 was beat by both players reaching the cave entrance in the top left corner
    and, if the level was completed, changes the scene to the beat level 1 screen
    Args:
        world(Level1): the current level appearing on the screen to access the player and cave entrances on the screen
    '''
    if colliding(world.player_1,world.cave_entrance_1) and colliding(world.player_2,world.cave_entrance_1):
        world.beat_L1 = True
        change_scene('beatL1')
def check_groundings(world:Level1):
    '''
    This function checks if the players are colliding with either the ground or a platform,
    changing their grounded status accordingly (this is used to prevent double jumping in the moving up functions)
    Args:
        world(Level1): the current level appearing on the screen to access the player and ground and platforms
    '''
    if colliding(world.player_1,world.ground):
        world.grounded_1 = True
        world.player_1.y = get_height()-40
        world.player_1.speed = 0
    elif not colliding(world.player_1,world.ground):
        world.grounded_1 = False
        for platform_L1 in world.platforms_L1:
            if colliding(world.player_1,platform_L1):
                world.player_1.y = platform_L1.y-30
                world.grounded_1 = True
    if colliding(world.player_2,world.ground):
        world.grounded_2 = True
        world.player_2.y = get_height()-40
        world.player_2.speed = 0
    elif not colliding(world.player_2,world.ground):
        world.grounded_2 = False
        for platform_L1 in world.platforms_L1:
            if colliding(world.player_2,platform_L1):
                world.player_2.y = platform_L1.y-30
                world.grounded_2 = True
def accelerate_player(world:Level1):
    '''
    This function simulates gravity, making the player fall faster the longer they are falling for, as gravity
    accelerates in real life, and applying gravity only when the player is not touching the ground or a platform
    Args:
        world(Level1): the current level the player is on in order to access their grounded status
        and alter their speeds and y coordinates
    '''
    if world.grounded_1:
        world.player_1.speed = 0
        world.player_1.y += world.player_1.speed
    elif not world.grounded_1:
        world.player_1.y += world.player_1.speed
        world.player_1.speed += 10
    if world.grounded_2:
        world.player_2.speed = 0
        world.player_2.y += world.player_2.speed
    elif not world.grounded_2:
        world.player_2.y += world.player_2.speed
        world.player_2.speed += 10

@starting
def create_level1() -> Level1:
    '''
    This function creates the first level and makes it appear on the screen and changes the background
    Returns:
        Level1: the first level of the game, containing the ground, the cave entrance, the platforms,
        the players and information about them, the flashlights, and an empty list of bats
    '''
    set_background_image(
        'https://cdna.artstation.com/p/assets/images/images/026/366/308/large/alicia-magistrello-basic-cave.jpg?1588597279')
    return Level1(create_ground(),
                  create_cave_entrance_1(), create_plat_L1(), False,
                  create_player1(), create_player2(), 3,3,display_health(),
                  True, True, False, False, False, False, "right","right",False, False, 0, 0,
                  create_p1_flashlight(), create_p2_flashlight(), False, False,
                  [])


when('typing', keys_pressed_p1)
when('done typing', keys_not_pressed_p1)
when('updating', move_player1)
debug()
