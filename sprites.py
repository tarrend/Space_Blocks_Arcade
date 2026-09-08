import pygame
from constants import *

# this file contains the different sprites for the game
class Ship(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # intial variables
        self.image_width = 100
        self.image = pygame.Surface((self.image_width, self.image_width))
        self.image.fill("#3b96eb")

        self.rect = self.image.get_rect(center=pygame.Vector2(WIDTH/2, HEIGHT-200))

        # related to movement
        self.position = pygame.Vector2(WIDTH/2, HEIGHT-200)
        self.speed = 250

    def movement(self, dt, key):

        direction = pygame.Vector2(0, 0)

        # get input
        if key[pygame.K_LEFT]:
            direction.x = -1
        elif key[pygame.K_RIGHT]:
            direction.x = 1
        else:
            direction.x = 0

        if key[pygame.K_UP]:
            direction.y = -1
        elif key[pygame.K_DOWN]:
            direction.y = 1
        else:
            direction.update

        # normalize and apply speed
        if direction.length() > 0:
            direction = direction.normalize()
        velocity = direction * self.speed

        # add this to position
        self.position += velocity * dt
        
        # set the rects center to the position
        self.rect.center = self.position

        # apply borders
        half_width = self.image_width/2



    def update(self, dt, key):
        self.movement(dt, key)
