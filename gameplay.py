import pygame
from random import randint, uniform
from constants import *
import sprites


# this script is dedicated for running gameplay elements
# however it does not contain sprites or many classes it is mainly just running
# that being said it does contain some basic objects

# groups
player_group = pygame.sprite.GroupSingle()
laser_group = pygame.sprite.Group()
meteor_group = pygame.sprite.Group()
alien_group = pygame.sprite.GroupSingle()
alien_laser_group = pygame.sprite.GroupSingle()
star_group = pygame.sprite.Group()
power_up_start_group = pygame.sprite.Group()
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

alien_timer = 0
alien_time = 25

star_timer = 0
star_time = 0.4
max_stars = 20

power_up_start_timer = 0
power_up_start_time = 60

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

    # aliens

    global alien_timer

    if alien_timer < alien_time:
        alien_timer += dt
    else:
        alien_timer -= alien_time
        alien_group.add(sprites.Alien())

    # stars

    global star_timer

    if len(star_group) < max_stars:
        if star_timer < star_time:
            star_timer += dt
        else:
            star_timer -= star_time
            star_group.add(sprites.Star())

    # power ups

    global power_up_start_timer

    if power_up_start_timer < power_up_start_time:
        power_up_start_timer += dt
    else:
        power_up_start_timer -= power_up_start_time
        power_up_start_group.add(sprites.PowerUp(pygame.Vector2(randint(0, WIDTH), -80)))

def shoot(key_just, position):
    # shoot at this stage does not just cover player shooting
    # it also covers the aliens being able to shoot

    global can_shoot

    if key_just[pygame.K_z] and can_shoot:
        laser_group.add(sprites.Laser(position))
        can_shoot = False

    # alien shooting
    alien = alien_group.sprite
    player = player_group.sprite
    if alien:
        if alien.position.x > alien.fire_point and not alien.fired:
            alien_laser_group.add(sprites.AlienLaser(alien.position, player.position))
            alien.fired = True

def collisions():
    # this function is required for checking the different collisions that can occur and handle them

    player = player_group.sprite

    # collision between laser and meteors
    laser_meteor_collision = pygame.sprite.groupcollide(laser_group, meteor_group, True, True)
    if laser_meteor_collision:
        player_collision_gain(laser_meteor_collision, 1, 10)

    # collision between laser and aliens
    laser_alien_collision = pygame.sprite.groupcollide(laser_group, alien_group, True, True)
    if laser_alien_collision:
        player_collision_gain(laser_alien_collision, 5, 50)
                    

    # collision between player and meteors
    player_meteor_collision = pygame.sprite.spritecollideany(player, meteor_group)
    if player_meteor_collision:
        player_collision_lose(player)

    # collision between player and aliens
    player_alien_collision = pygame.sprite.spritecollideany(player, alien_group)
    if player_alien_collision:
        player_collision_lose(player)

    # collision between player and alien lasers
    player_alien_laser_collision = pygame.sprite.spritecollideany(player, alien_laser_group)
    if player_alien_laser_collision:
        player_collision_lose(player)
        

def player_collision_lose(player):

    global score
    # collision occured

    # reset the meteors, aliens, alien lasers and score
    meteor_group.empty()
    alien_group.empty()
    alien_laser_group.empty()
    score = 0
            
    # add an explosion
    explosion_group.append(sprites.Explosion(player.position))

def player_collision_gain(collisions, default_amount, gold_amount):

    global score

    for objects in collisions.values():
        for object in objects:

            # increase score
            if object.is_golden:
                score += gold_amount
            else:
                score += default_amount

            explosion_group.append(sprites.Explosion(object.position))



def updating(dt, key, key_just):

    # the reason why screen is passed here is because the explosions require it
    # they are not traditional sprites and require pygame.draw.circle in them
    # the reason they aren't in rendering is because ideally the explosion should continue while paused

    # updating the different groups
    player_group.update(dt, key)
    laser_group.update(dt)
    meteor_group.update(dt)
    alien_group.update(dt)
    alien_laser_group.update(dt)
    star_group.update(dt)
    power_up_start_group.update(dt)

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
    star_group.draw(screen)
    for star in star_group.sprites():
        star.display_extras(screen)
    player.display_extras(screen)
    player_group.draw(screen)

    laser_group.draw(screen)
    meteor_group.draw(screen)
    alien_group.draw(screen)

    for alien in alien_group.sprites():
        alien.display_extras(screen)

    alien_laser_group.draw(screen)

    power_up_start_group.draw(screen)


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
