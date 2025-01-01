import pygame
import data_file
import sys
import os 
import random

sys.path.append(os.path.abspath('modules'))

import inventory


pygame.init()


player = data_file.PlayerObject(350, 250, "player_animation", "player_animation/", 7)
bg = data_file.BackgroundObject(100, 0, "objects/bg_1.png", player)

objects = [
    data_file.Stone(random.randint(0, 500), random.randint(0, 500), 'using_objects/pickaxe.png', 100, player),
    data_file.HostileNPC_Object(random.randint(0, 500), random.randint(0, 500), 'player_animation', 'player_animation/', 5, player)
]

items = [
    data_file.DropedItem(random.randint(0, 500), random.randint(0, 500), 'using_objects/pickaxe.png', data_file.Pickaxe('using_objects/pickaxe.png', 1), player),
]

def draw(screen):
    bg.draw(screen)
    player.draw(screen)

    for i in objects:
        i.draw(screen)

    for i in items:
        i.draw(screen)

    inventory.load(screen, player)