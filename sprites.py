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

        # related to movement
        self.position = pygame.Vector2(WIDTH/2, HEIGHT-200)
        self.speed = 250

        # different parts of the ship
        self.wing_rect = pygame.Rect((0, 0), (70, 15))
        self.wing_rect_2 = self.wing_rect.copy()
        self.laser_gun_rect = pygame.Rect((0, 0), (16, 12))

        self.set_extra_locations()

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
        self.set_extra_locations()

        # set the rects center to the position
        self.rect.center = self.position

    def set_extra_locations(self):
        self.wing_rect.center = pygame.Vector2(self.position.x-self.image_width_half, self.position.y)
        self.wing_rect_2.center = pygame.Vector2(self.position.x+self.image_width_half, self.position.y)
        
        self.laser_gun_rect.center = pygame.Vector2(self.position.x, self.position.y-self.image_width_half-6)
                

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

        self.is_golden = False

        self.image = pygame.Surface((random_size, random_size))

        # determine if the meteor will be golden
        if randint(1, 25) == 25:
            self.image.fill("darkgoldenrod2")
            self.is_golden = True
        else:
            self.image.fill("azure3")
            self.is_golden = False

        self.rect = self.image.get_rect()

        # movement
        self.position = pygame.Vector2(randint(0, WIDTH), randint(-120, -80))
        self.speed = randint(250, 300)
        self.direction = pygame.Vector2(uniform(-0.2, 0.2), 1).normalize()

        self.rect.center = self.position

    def movement(self, dt):

        # move the meteor
        velocity = self.direction * self.speed
        self.position += velocity * dt

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

        self.image = pygame.Surface((10, 50))
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
        if self.position.y < -50:
            self.kill()

    def update(self, dt):
        self.movement(dt)

class Alien(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # initial variables
        
        self.image = pygame.Surface((150, 50))
        self.image.fill("#5195b0")

        self.rect = self.image.get_rect()

        # movement
        self.speed = randint(100, 250)
        self.position = pygame.Vector2(randint(-120, -90), randint(90, 120))

        self.rect.center = self.position

        # different parts
        self.glass_rect = pygame.Rect(0, 0, 70, 50)
        self.bottom_piece_rect = pygame.Rect(0, 0, 70, 25)
        self.square_rect = pygame.Rect(0, 0, 20, 20)

        self.alien_rect = pygame.Rect(0, 0, 35, 35)
        self.alien_eye_rect = pygame.Rect(0, 0, 7, 7)
        self.alien_eye_rect_2 = self.alien_eye_rect.copy()

        self.set_extras_locations()

    def set_extras_locations(self):
        self.glass_rect.midbottom = pygame.Vector2(self.position.x, self.position.y-25)
        self.bottom_piece_rect.midtop = pygame.Vector2(self.position.x, self.position.y+25)
        self.square_rect.center = pygame.Vector2(self.position.x, self.position.y)
        self.alien_rect.midbottom = pygame.Vector2(self.position.x, self.position.y-25)
        self.alien_eye_rect.center = pygame.Vector2(self.position.x-7, self.position.y-50)
        self.alien_eye_rect_2.center = pygame.Vector2(self.position.x+7, self.position.y-50)

    def movement(self, dt):

        self.position.x += self.speed * dt

        if self.position.x > WIDTH + 60:
            self.kill()

        self.rect.center = self.position

        # make the extra parts stay along
        self.set_extras_locations()

        # despawn the alien when it is off screen
        if self.position.x > WIDTH + 400:
            self.kill()



    def display_extras(self, screen):
        pygame.draw.rect(screen, "#03cffc", self.glass_rect)
        pygame.draw.rect(screen, "#5195b0", self.bottom_piece_rect)
        pygame.draw.rect(screen, "#2fd379", self.square_rect)
        pygame.draw.rect(screen, "#51c083", self.alien_rect)
        pygame.draw.rect(screen, "black", self.alien_eye_rect)
        pygame.draw.rect(screen, "black", self.alien_eye_rect_2)

    def update(self, dt):
        self.movement(dt)

class Explosion():
    def __init__(self, position):
        # this is very important to note
        # this class is technically not a pygame sprite
        # however its similar enough to be in this file as it like the other sprites shows up on screen
        # and has self contained functionality

        # initial variables
        self.position = position
        self.radius_size = 0

        # controlling size of the explosion
        self.max_size = 50
        self.increment_amount = 5
        self.increasing = True

        # also note that the increment amount may not be accurate to pixels
        # its just a general measurement for increase and decrease

        self.adjusted_increment = self.increment_amount * 100


        self.colour = "#f56f0f"

        self.destroy = False

    def update(self, dt):

        if self.increasing:
            
            self.radius_size += self.adjusted_increment * dt

            # check ifu the explosion should start decreasing
            if self.radius_size > self.max_size:
                self.increasing = False
        else:
            self.radius_size -= self.adjusted_increment * dt

        if not self.radius_size >= 1:
            self.destroy = True

    def draw(self, screen):

        pygame.draw.circle(screen, self.colour, self.position, self.radius_size)
