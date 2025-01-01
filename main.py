import pygame
import data_file
import sys
import os

sys.path.append(os.path.abspath('modules/levels'))

import test_level


pygame.init()


levels = [
    test_level,
]


fps = pygame.time.Clock()
screen = pygame.display.set_mode((800, 600))
title = pygame.display.set_caption("Rpg Demo")
current_level = test_level
level_count = 0

def next_level():
    global level_count
    global levels
    global current_level

    level_count += 1

    if level_count > len(levels):
        level_count = len(levels)

    current_level = levels[level_count]


running = True
while running:
    key = pygame.key.get_pressed()


    fps.tick(15)


    screen.fill('black')
    

    current_level.draw(screen)


    if key[pygame.K_F5]:
        if not len(levels) == 1:
            next_level()


    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
