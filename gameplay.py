import pygame
from random import uniform
from constants import *
import sprites


# this script is dedicated for running gameplay elements
# however it does not contain sprites or many classes it is mainly just running
# that being said it does contain some basic objects

# groups
player_group = pygame.sprite.GroupSingle()
laser_group = pygame.sprite.Group()
meteor_group = pygame.sprite.Group()
explosion_group = []

# add player to their group
player_group.add(sprites.Ship())
player = player_group.sprite

# title text
title_text_font = pygame.Font(None, 50)
title_text_surface = title_text_font.render("Space Blocks Arcade!", True, "white")
title_text_rect = title_text_surface.get_rect(center = pygame.Vector2(WIDTH/2, 100))

size_35_font = pygame.Font(None, 35)

# different game timers and systems
shoot_timer = 0
shoot_time = 1
can_shoot = True

meteor_timer = 0
meteor_time = 0.2

# score
score = 0

# pause
pause = False

def timers(dt):

    # shooting
    global shoot_timer
    global can_shoot

    if not can_shoot:
        if shoot_timer < shoot_time:
            shoot_timer += dt
        else:
            shoot_timer -= shoot_time
            can_shoot = True

    # meteors
    global meteor_timer
    global meteor_time


    if meteor_timer < meteor_time:
        meteor_timer += dt
    else:
        meteor_timer -= meteor_time
        meteor_time = uniform(0.2, 0.5)

        # add the meteor
        meteor_group.add(sprites.Meteor())

def shoot(key_just, position):

    global can_shoot

    if key_just[pygame.K_z] and can_shoot:
        laser_group.add(sprites.Laser(position))
        can_shoot = False

def collisions():
    # this function is required for checking the different collisions that can occur and handle them

    global score

    player = player_group.sprite

    # collision between laser and meteors
    laser_meteor_collision = pygame.sprite.groupcollide(laser_group, meteor_group, True, True)
    if laser_meteor_collision:
        for meteors in laser_meteor_collision.values():
            for meteor in meteors:

                # increase the score
                if meteor.is_golden:
                    score += 10
                else:
                    score += 1

                # there will be extra stuff here later on such as an explosion effect
                # for now this is all that the code here does
                explosion_group.append(sprites.Explosion(meteor.position))

    # collision between player and meteors
    player_meteor_collision = pygame.sprite.spritecollideany(player, meteor_group)
    if player_meteor_collision:
        # collision occured

        # reset the meteors and score
        meteor_group.empty()
        score = 0

        # add an explosion
        explosion_group.clear()
        explosion_group.append(sprites.Explosion(player.position))

def updating(dt, key, key_just):

    # the reason why screen is passed here is because the explosions require it
    # they are not traditional sprites and require pygame.draw.circle in them
    # the reason they aren't in rendering is because ideally the explosion should continue while paused

    # updating the different groups
    player_group.update(dt, key)
    laser_group.update(dt)
    meteor_group.update(dt)

    # run the different game timers
    timers(dt)

    # shooting mechanic
    laser_spawn_pos = player.position.copy()
    laser_spawn_pos.y -= 40
    shoot(key_just, laser_spawn_pos)

    # handling collisions
    collisions()

    # handling explosions
    for i, explosion in enumerate(explosion_group):

        if explosion.destroy:
            explosion_group.pop(i)
            continue
        explosion.update(dt)

def rendering(screen):

    # rendering the different groups
    player.display_extras(screen)
    player_group.draw(screen)

    laser_group.draw(screen)
    meteor_group.draw(screen)



    # displaying different text
    screen.blit(title_text_surface, title_text_rect)


    # score text
    score_surface = size_35_font.render("Score: " + str(score), True, "#fcea42")
    screen.blit(score_surface, pygame.Vector2(50, 50))

    # reloading text
    if not can_shoot:
        reloading_time = shoot_time - shoot_timer
        if reloading_time <= 0:
            reloading_time = 0
        reloading_text_text = f"Reloading... ({reloading_time:.1f})"
        reloading_text_surface = size_35_font.render(reloading_text_text, True, "#c90e1e")
        screen.blit(reloading_text_surface, pygame.Vector2(50, 100))

    # handling explosion
    for explosion in explosion_group:
        explosion.draw(screen)



def run(screen, dt, key, key_just):

    global pause

    if not pause:
        # only continue updating the game if its not paused
        updating(dt, key, key_just)

    rendering(screen)

    # check if the player decides to pause the game
    if key_just[pygame.K_SPACE]:
        pause = not pause
