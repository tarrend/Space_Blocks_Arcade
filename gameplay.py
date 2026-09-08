import pygame
from constants import *
import sprites


# this script is dedicated for running gameplay elements
# however it does not contain sprites or many classes it is mainly just running
# that being said it does contain some basic objects

# groups
player_group = pygame.sprite.GroupSingle()

# add sprites to groups
player_group.add(sprites.Ship())

# title text
title_text_font = pygame.Font(None, 50)
title_text_surface = title_text_font.render("Space Blocks Arcade!", True, "white")
title_text_rect = title_text_surface.get_rect(center = pygame.Vector2(WIDTH/2, 100))

def rendering(screen):

    # displaying different text
    screen.blit(title_text_surface, title_text_rect)

    # rendering the different groups
    player_group.draw(screen)
    

def updating():
    pass

def run(screen):
    rendering(screen)
    updating()
