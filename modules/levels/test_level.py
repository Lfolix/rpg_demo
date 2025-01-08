import pygame
import data_file
import sys
import os 
import random
sys.path.append(os.path.abspath('modules/levels'))
sys.path.append(os.path.abspath('modules'))
import interface

import inventory


pygame.init()


player = data_file.PlayerObject(350, 250, "player_animation", "player_animation/", 7, 100)
bg = data_file.BackgroundObject(100, 0, "objects/bg_1.png", player)

objects = [
    data_file.Stone(random.randint(0, 500), random.randint(0, 500), 'using_objects/pickaxe.png', 100, player),
]

items = [
    data_file.DropedItem(random.randint(0, 500), random.randint(0, 500), 'using_objects/pickaxe.png', data_file.Pickaxe('using_objects/pickaxe.png', 1), player),
    data_file.DropedItem(random.randint(0, 500), random.randint(0, 500), 'using_objects/poor_quality_bow.png', data_file.PoorQualityBow('using_objects/poor_quality_bow.png'), player),
]

def draw(screen):
    bg.draw(screen)
    player.draw(screen)

    for i in objects:
        i.draw(screen)

    for i in items:
        i.draw(screen)

    interface.draw(screen, player)

    inventory.load(screen, player)