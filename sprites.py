import pygame
from constants import *

# this file contains the different sprites for the game
class Ship(pygame.sprite.Sprite):
    def __init__(self, size, rect_size):
        super().__init__()

        # intial variables
        self.image = pygame.Surface(size)
        self.image = pygame.transform.rotate(self.image, 45)
        self.image.fill("#3b96eb")

        self.rect = pygame.Rect((0, 0), rect_size)
        self.rect.center = pygame.Vector2(WIDTH/2, HEIGHT-100)


