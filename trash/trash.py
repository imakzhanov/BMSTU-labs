import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Прямоугольник
x, y = 100, 250
speed = 5
direction = 1  # 1 - вправо, -1 - влево

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Движение
    x += speed * direction

    # Отскок от границ
    if x > 700 or x < 0:
        direction *= -1

    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (255, 0, 0), (x, y, 50, 50))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()