import pygame
from constants import *
import sprites


# this script is dedicated for running gameplay elements
# however it does not contain sprites or many classes it is mainly just running
# that being said it does contain some basic objects

# groups
player_group = pygame.sprite.GroupSingle()
laser_group = pygame.sprite.Group()

# add sprites to groups
player_group.add(sprites.Ship())
player = player_group.sprite

# title text
title_text_font = pygame.Font(None, 50)
title_text_surface = title_text_font.render("Space Blocks Arcade!", True, "white")
title_text_rect = title_text_surface.get_rect(center = pygame.Vector2(WIDTH/2, 100))

def rendering(screen):
    # rendering the different groups
    player.display_extras(screen)
    player_group.draw(screen)

    laser_group.draw(screen)



    # displaying different text
    screen.blit(title_text_surface, title_text_rect)

# different game timers and systems
shoot_timer = 0
shoot_time = 0.5
can_shoot = True

def timers(dt):

    # shooting
    global shoot_timer
    global can_shoot

    if shoot_timer < shoot_time:
        shoot_timer += dt
    else:
        shoot_timer -= shoot_time

        if not can_shoot:
            can_shoot = True

def shoot(key_just, position):

    global can_shoot

    if key_just[pygame.K_z] and can_shoot:
        laser_group.add(sprites.Laser(position))
        can_shoot = False

def updating(dt, key, key_just):

    # updating the different groups
    player_group.update(dt, key)
    laser_group.update(dt)

    # run the different game timers
    timers(dt)

    # shooting mechanic
    laser_spawn_pos = player.position.copy()
    laser_spawn_pos.y -= 40
    shoot(key_just, laser_spawn_pos)

def run(screen, dt, key, key_just):
    updating(dt, key, key_just)
    rendering(screen)
