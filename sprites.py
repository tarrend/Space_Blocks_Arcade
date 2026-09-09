import pygame
from random import randint, uniform
from constants import *


# this file contains the different sprites for the game
class Ship(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # intial variables
        self.image_width = 50
        self.image_width_half = self.image_width/2
        self.image = pygame.Surface((self.image_width, self.image_width))
        self.image.fill("#3b96eb")

        self.rect = self.image.get_rect(center=pygame.Vector2(WIDTH/2, HEIGHT-200))

        # wings and laser gun
        self.wing_rect = pygame.Rect((0, 0), (70, 15))
        self.wing_rect_2 = self.wing_rect.copy()

        self.wing_rect.center = pygame.Vector2(WIDTH/2-self.image_width_half, HEIGHT-200)
        self.wing_rect_2.center = pygame.Vector2(WIDTH/2+self.image_width_half, HEIGHT-200)

        self.laser_gun_rect = pygame.Rect((0, 0), (16, 12))
        self.laser_gun_rect.center = pygame.Vector2(WIDTH/2, HEIGHT-206-self.image_width_half)

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

        # apply borders
        if self.position.x - self.image_width_half < 0:
            self.position.x = self.image_width_half
        if self.position.x + self.image_width_half > WIDTH:
            self.position.x = WIDTH - self.image_width_half
        if self.position.y - self.image_width_half < 0:
            self.position.y = self.image_width_half
        if self.position.y + self.image_width_half > HEIGHT:
            self.position.y = HEIGHT - self.image_width_half

        # change the position of the parts of the sprite
        self.wing_rect.center = pygame.Vector2(self.position.x-self.image_width_half, self.position.y)
        self.wing_rect_2.center = pygame.Vector2(self.position.x+self.image_width_half, self.position.y)

        self.laser_gun_rect.center = pygame.Vector2(self.position.x, self.position.y-self.image_width_half-6)
        
        # set the rects center to the position
        self.rect.center = self.position

    def display_extras(self, screen):

        # draw wings
        pygame.draw.rect(screen, "#204de3", self.wing_rect)
        pygame.draw.rect(screen, "#204de3", self.wing_rect_2)

        # draw laser gun
        pygame.draw.rect(screen, "#eb4c1c", self.laser_gun_rect)

    def update(self, dt, key):
        self.movement(dt, key)

class Meteor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # initial variables

        random_size = randint(40, 60)

        self.image = pygame.Surface((random_size, random_size))
        self.image.fill("azure3")
        self.rect = self.image.get_rect()

        # movement
        self.position = pygame.Vector2(randint(0, WIDTH), randint(-120, -80))
        self.speed = randint(150, 200)
        self.direction = pygame.Vector2(uniform(-1, 1), 1).normalize()

        self.rect.center = self.position

    def movement(self, dt):

        # move the meteor
        velocity = self.direction * self.speed
        self.position += velocity * dt
        print(self.position)

        # move the rect to the position
        self.rect.center = self.position

        # despawn the meteor
        if self.position.y > HEIGHT + 65:
            self.kill()

    def update(self, dt):
        self.movement(dt)

class Laser(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()

        # initial variables

        self.image = pygame.Surface((4, 24))
        self.image.fill("#ffdd30")
        self.rect = self.image.get_rect()

        # positioning
        self.position = position
        self.speed = 800

        self.rect.center = self.position

    def movement(self, dt):

        # move upwards
        self.position.y -= self.speed * dt

        self.rect.center = self.position

        # check if the laser is off screen, if it is destroy the laser
        if self.position.y < -20:
            self.kill()

    def update(self, dt):
        self.movement(dt)
