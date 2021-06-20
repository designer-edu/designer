import pygame


class Director:
    def __init__(self, width=800, height=600, background_color=(255, 255, 255)):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        self.bkgr_color = background_color
        self.screen.fill(background_color)

        self.background = pygame.Surface(self.screen.get_size()).convert()

        self.running = False
        self.all_game_sprites = pygame.sprite.LayeredDirty()

    def start(self):
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

dir = Director()
dir.start()