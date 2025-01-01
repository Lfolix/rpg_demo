import pygame
import sys

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 800, 600
TILE_SIZE = 32  # Размер плитки
FPS = 60

# Загрузка изображений плиток
grass_image = pygame.image.load('objects/parameters.png')
water_image = pygame.image.load('objects/bg_1.png')
dirt_image = pygame.image.load('objects/bg_1.png')

# Создание двумерного массива для представления карты
tilemap = [
    [0, 0],
]

# Словарь для сопоставления значений плиток с изображениями
tile_images = {
    0: grass_image,  # 0 - трава
    1: water_image,  # 1 - вода
    2: dirt_image,   # 2 - земля
}

# Создание экрана
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tilemap Example")

# Основной игровой цикл
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Отрисовка карты
    for y, row in enumerate(tilemap):
        for x, tile in enumerate(row):
            screen.blit(tile_images[tile], (x * TILE_SIZE, y * TILE_SIZE))

    pygame.display.flip()
    clock.tick(FPS)
