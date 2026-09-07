import pygame
from constants import *

# initial variables
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Blocks Arcade")
clock = pygame.time.Clock()
dt = 0
running = True


# main loop
while running:

    # calculating dt
    dt = clock.tick(FPS) / 1000

    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False

    # game updating and rendering
    screen.fill("#0d002b")

    pygame.display.update()

# quit pygame
pygame.quit()
