import pygame
from constants import *

# this file contains the different sprites for the game
class Ship(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # intial variables
        self.image = pygame.Surface((50, 50))
        self.image = pygame.transform.rotate(self.image, 45)
        self.image.fill("#3b96eb")

        self.rect = pygame.Rect((0, 0), (40, 40))
        self.rect.center = pygame.Vector2(WIDTH/2, HEIGHT-200)


