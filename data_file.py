import pygame
import os
import re


pygame.init()


def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', s)] 

#Basic objects

class Object:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

class BackgroundObject(Object):
    def __init__(self, x, y, image, player):
        super().__init__(x, y, image)
        self.player = player

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
        self.camera(pygame.key.get_pressed())

    def camera(self, key):
        if key[pygame.K_w]:
            self.y += self.player.speed
        
        if key[pygame.K_s]:
            self.y -= self.player.speed

        if key[pygame.K_a]:
            self.x += self.player.speed

        if key[pygame.K_d]:
            self.x -= self.player.speed

class CameraObject(Object):
    def __init__(self, x, y, image, player):
        super().__init__(x, y, image)
        self.player = player

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))


#Gui objects

class Text:
    def __init__(self, text, size, color, x, y):
        self.text = pygame.font.Font(None, size).render(text, True, color)
        self.x, self.y = x, y

    def draw(self, screen):
        screen.blit(self.text, (self.x, self.y))

class ButtonObject(Object):
    def __init__(self, x, y, text : Text, function):
        self.x, self.y = x, y
        self.image = pygame.image.load('objects/Button.png')
        self.text = text
        self.function = function
        self.rect = self.image.get_rect()

    def draw(self, screen, mouse, mouse_key):
        self.text.draw(self.image)
        screen.blit(self.image, (self.x, self.y))

        if self.rect.collidepoint(mouse[0], mouse[1]):
            if mouse_key[0]:
                self.function()




#Hard objects

class AliveObject:
    def __init__(self, x, y, directory_animation, file_path, speed, health):
        self.x = x
        self.y = y
        self.directory_animation = os.listdir(directory_animation)
        self.directory_animation.sort(key = natural_sort_key)
        self.file_path = file_path
        self.speed = speed
        self.health = health

        self.anim_down = [
            pygame.image.load(f'{self.file_path}{self.directory_animation[0]}'),
            pygame.image.load(f'{self.file_path}{self.directory_animation[1]}'),
            pygame.image.load(f'{self.file_path}{self.directory_animation[2]}'),
            pygame.image.load(f'{self.file_path}{self.directory_animation[3]}'),
        ]

        self.anim_left = [
            pygame.image.load(f'{self.file_path}{self.directory_animation[4]}'),
            pygame.image.load(f'{self.file_path}{self.directory_animation[5]}'),
            pygame.image.load(f'{self.file_path}{self.directory_animation[6]}'),
            pygame.image.load(f'{self.file_path}{self.directory_animation[7]}'),
        ]

        self.anim_right = [
            pygame.image.load(f'{self.file_path}{self.directory_animation[8]}'),
            pygame.image.load(f'{self.file_path}{self.directory_animation[9]}'),
            pygame.image.load(f'{self.file_path}{self.directory_animation[10]}'),
            pygame.image.load(f'{self.file_path}{self.directory_animation[11]}'),
        ]

        self.anim_up = [
            pygame.image.load(f'{self.file_path}{self.directory_animation[12]}'),
            pygame.image.load(f'{self.file_path}{self.directory_animation[13]}'),
            pygame.image.load(f'{self.file_path}{self.directory_animation[14]}'),
            pygame.image.load(f'{self.file_path}{self.directory_animation[15]}'),
        ]

        self.anim_count = 0
        self.direction = self.anim_down

        self.rect = pygame.rect.Rect(self.x, self.y, 64, 64) 

    def update_animation(self):
        self.anim_count += 1

        if self.anim_count == 4:
            self.anim_count = 0

class PlayerObject(AliveObject):
    def __init__(self, x, y, directory_animation, file_path, speed, health):
        super().__init__(x, y, directory_animation, file_path, speed, health)

        self.disable_inventory = list()
        self.enable_inventory = list()
        self.xp = 0
        self.hunger = 100

    def draw(self, screen):
        if self.health > 0:
            self.hunger -= 0.01
            self.rect.topleft = (self.x, self.y)
            print(self.disable_inventory)
            screen.blit(self.direction[self.anim_count], (370, 270))
            self.anim_walk(pygame.key.get_pressed())
            self.update_animation()

    def anim_walk(self, key):
        if key[pygame.K_w]:
            self.direction = self.anim_up

        elif key[pygame.K_s]:
            self.direction = self.anim_down

        elif key[pygame.K_a]:
            self.direction = self.anim_left

        elif key[pygame.K_d]:
            self.direction = self.anim_right
    
        elif not any(key):
            self.anim_count = 1

class HostileNPC_Object(AliveObject):
    def __init__(self, x, y, directory_animation, file_path, speed, player, health):
        super().__init__(x, y, directory_animation, file_path, speed, health)
        self.player = player

    def follow(self):
        if self.health > 0:
            # Вычисляем разницу между позициями NPC и игрока
            delta_x = self.player.x - self.x
            delta_y = self.player.y - self.y

            # Двигаемся по оси X сначала
            if abs(delta_x) > abs(delta_y):
                if delta_x > 0:
                    self.direction = self.anim_right
                    self.x += self.speed
                else:
                    self.direction = self.anim_left
                    self.x -= self.speed
                # После движения по X, проверяем Y
                if self.player.y > self.y:
                    self.direction = self.anim_down
                    self.y += self.speed
                elif self.player.y < self.y:
                    self.direction = self.anim_up
                    self.y -= self.speed
            else:
                # Двигаемся по оси Y сначала
                if delta_y > 0:
                    self.direction = self.anim_down
                    self.y += self.speed
                else:
                    self.direction = self.anim_up
                    self.y -= self.speed
                # После движения по Y, проверяем X
                if self.player.x > self.x:
                    self.direction = self.anim_right
                    self.x += self.speed
                elif self.player.x < self.x:
                    self.direction = self.anim_left
                    self.x -= self.speed

    def camera(self, key):
        if key[pygame.K_w]:
            self.y += self.player.speed
        
        if key[pygame.K_s]:
            self.y -= self.player.speed

        if key[pygame.K_a]:
            self.x += self.player.speed

        if key[pygame.K_d]:
            self.x -= self.player.speed

    def draw(self, screen):
        screen.blit(self.direction[self.anim_count], (self.x, self.y))
        self.follow()
        self.camera(pygame.key.get_pressed())
        self.update_animation()

# Item objects

class Item:
    def __init__(self, image):
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.show_parameters = True
        self.not_show_parameters = False

    def draw(self, screen, slot):
        self.rect.topleft = slot
        screen.blit(self.image, (slot))

class Tool(Item):
    def __init__(self, image):
        super().__init__(image)

    def return_parameters(self):
        return [Text(f'Mining : {self.mining}', 20, ('Red'), 10, 20)]
    
class Pickaxe(Item):
    def __init__(self, image, speed):
        super().__init__(image)
        self.type = 'pickaxe'
        self.speed = speed

    def return_parameters(self):
        return [Text(f'Speed : {str(self.speed)}', 20, ('Red'), 10, 20)]
    
class PoorQualityBow(Item):
    def __init__(self, image):
        super().__init__(image)
        self.type = "bow"
        self.attack = 10
        self.speed = 1

    def return_parameters(self):
        return [Text(f'Attack : {str(self.attack)}', 20, ('Red'), 10, 20), Text(f'Speed : {str(self.speed)}', 20, ('Blue'), 35, 20)]

class DropedItem:
    def __init__(self, x, y, image, item, player):
        self.x, self.y, self.image = x, y, pygame.image.load(image)
        self.item = item
        self.player = player
        self.rect = pygame.rect.Rect(self.x, self.y, 1, 1)
        self.alive = True
    
    def draw(self, screen):
        if self.alive:
            self.rect.topleft = self.x, self.y
            screen.blit(self.image, (self.x, self.y))

            self.IsTake()
            self.camera(pygame.key.get_pressed())

    def IsTake(self):
        if self.player.rect.colliderect(self.rect):
            self.x = 1343245
            self.y = 3465345
            self.rect.center = self.y, self.x
            
            self.player.disable_inventory.append(self.item)

    def camera(self, key):
        if key[pygame.K_w]:
            self.y += self.player.speed
        
        if key[pygame.K_s]:
            self.y -= self.player.speed

        if key[pygame.K_a]:
            self.x += self.player.speed

        if key[pygame.K_d]:
            self.x -= self.player.speed

# Mining objects

class MineObject(CameraObject):
    def __init__(self, x, y, image, player):
        super().__init__(x, y, image, player)
        self.rect = self.image.get_rect()
        self.player = player

class Stone(MineObject):
    def __init__(self, x, y, image, health, player):
        super().__init__(x, y, image, player)
        self.health = health

    def mine(self, mouse):
        if self.player.rect.colliderect(self.rect):
            if self.rect.collidepoint(mouse.get_pos()[0], mouse.get_pos()[1]):
                if mouse.get_pressed()[0]:
                    if len(self.player.enable_inventory) > 0:
                        if self.player.enable_inventory[0].type == 'pickaxe':
                            if self.health > 0:
                                self.health -= self.player.enable_inventory[0].speed
                                print("ok")

    def camera(self, key):
        if key[pygame.K_w]:
            self.y += self.player.speed
        
        if key[pygame.K_s]:
            self.y -= self.player.speed

        if key[pygame.K_a]:
            self.x += self.player.speed

        if key[pygame.K_d]:
            self.x -= self.player.speed

    def draw(self, screen):
        self.rect.topleft = self.x, self.y
        print(self.health)
        if self.health > 0:
            Text(str(self.health), 15, 'Blue', self.x, self.y).draw(screen)
            screen.blit(self.image, (self.x, self.y))

        self.camera(pygame.key.get_pressed())
        self.mine(pygame.mouse)

        
        
        

