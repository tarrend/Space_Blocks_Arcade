import pygame
from constants import *


# this script is dedicated for running gameplay elements
# however it does not contain sprites or many classes it is mainly just running
# that being said it does contain some basic objects

title_text_font = pygame.Font(None, 30)
title_text_surface = title_text_font.render("Space Blocks Arcade!", False, "white")
title_text_rect = title_text_surface.get_rect()
title_text_rect.center = pygame.Vector2(WIDTH/2, 150)

def run():
    print("running")
