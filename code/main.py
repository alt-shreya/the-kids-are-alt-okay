from tkinter import Button
import pygame
import sys

from settings import *
from debug import debug
from level import Level


class Game:
    def __init__(self):

        # general setup
        pygame.init()
        # create a display surface
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('The Kids are Alt-okay')
        # create a clock
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        self.efont = pygame.font.Font(EXPLAIN_FONT, EXPLAIN_FONT_SIZE)
        self.level = Level()
        self.intro_background = pygame.image.load(
            '02 - setup/2 - setup/code/graphics/intro/bg.png')

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.level.toggle_menu()

            self.screen.fill(WATER_COLOR)
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)


# check if the file is main, then create an instant of class Game
if __name__ == '__main__':
    game = Game()
    game.run()
