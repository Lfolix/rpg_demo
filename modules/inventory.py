import pygame
import data_file
import time


pygame.init()


inventory_image = pygame.image.load('using_objects/inventory_image.png')

tiles = [
    (285, 275),
    (285, 385),
    (285, 485),
]

current_tiles = [
    (70, 280),
    (65, 410)
]

alive = False

parameters = pygame.image.load('objects/parameters.png')
item_menu = pygame.image.load('objects/item_menu.png')

def delete_item(i, pl):
    pl.disable_inventory.remove(i)


del_btn = data_file.ButtonObject(0, 0, data_file.Text('j', 10, "Black", 10, 10), delete_item)





def load(screen, player):
    mouse_rect = pygame.Rect(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 16, 16)

    global alive

    sur_slot = -1

    mouse = pygame.mouse.get_pressed()
    mouse_pos = pygame.mouse.get_pos()
    key = pygame.key.get_pressed()

    if key[pygame.K_i]:
        time.sleep(0.2)

        alive = not alive  # Переключаем состояние alive

    if alive:
        screen.blit(inventory_image, (0, 0))

        for i in player.disable_inventory:

            if mouse_rect.colliderect(i.rect):
                for event in pygame.event.get():
                    if mouse[0]:
                        if i in player.disable_inventory:
                            del_item = i
                            player.disable_inventory.remove(i)
                            player.enable_inventory.append(del_item)
                            print("ok")

                    if mouse[1]:
                        player.inventory.remove(i)


            sur_slot += 1
            i.draw(screen, tiles[sur_slot])  # Здесь i - это объект Item, который должен иметь метод draw


        for i in player.enable_inventory:

            if mouse_rect.colliderect(i.rect):
                if not i.not_show_parameters:
                    i.show_parameters = True
                else:
                    i.show_parameters = False

                for event in pygame.event.get():
                    if mouse[0]:  # ЛКМ
                        if i in player.enable_inventory:
                            del_item = i
                            player.enable_inventory.remove(i)
                            player.disable_inventory.append(del_item)
                            print("ok")

                    if mouse[2]:  # ПКМ
                        if not i.not_show_parameters:
                            i.not_show_parameters = True  # Устанавливаем состояние, чтобы скрыть параметры

                        else:
                            i.not_show_parameters = False

                    if mouse[1]:
                        player.inventory.remove(i)

                # Отображаем параметры только если show_parameters истинно
                if i.show_parameters and not i.not_show_parameters:
                    screen.blit(item_menu, (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]))

                    if i.show_parameters:
                        for j in i.return_parameters():
                            j.draw(parameters)


                if i.not_show_parameters and not i.show_parameters:
                    del_btn.draw(parameters, mouse_pos, mouse)
                    screen.blit(parameters, (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]))


            # Отрисовка предмета
            sur_slot = -1
            print(i)

            sur_slot += 1
            i.draw(screen, current_tiles[sur_slot])  # Здесь i - это объект Item, который должен иметь метод draw
