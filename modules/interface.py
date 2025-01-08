import pygame
import data_file


pygame.init()


def draw(screen, player):

    list = [
        data_file.Text(f'Health: {player.health}', 20, "red", 0, 0),
        data_file.Text(f'Xp: {player.xp}', 20, "green", 0, 20),
        data_file.Text(f'Hunger: {player.health}', 20, "brown", 0, 40),
    ]

    for i in list:
        i.draw(screen)
