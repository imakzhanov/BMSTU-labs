import sys

import pygame
from math import sin

pygame.init()

screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

step = 2
cur_pos = 0

START_X = -100
CENTER_Y = 200
AMPLITUDE = 80
SPEED_WAVE = 0.03

# ---------------------------------
# 3 звезды: x, y
# ---------------------------------
stars = [
    [120, 80],
    [300, 140],
    [520, 60]
]

star_index = 0     # какая звезда сейчас увеличивается
star_size = 2      # текущий радиус активной звезды
grow = True        # растёт ли звезда сейчас

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((15, 20, 50))

    # ---------------------------------
    # рисуем звёзды
    # ---------------------------------
    for i in range(len(stars)):
        x_star = stars[i][0]
        y_star = stars[i][1]

        if i == star_index:
            radius = star_size   # активная звезда увеличивается
        else:
            radius = 2           # остальные обычные

        pygame.draw.circle(screen, (255, 255, 255), (x_star, y_star), radius)

    # ---------------------------------
    # анимация звёзд по очереди
    # ---------------------------------
    if grow:
        star_size += 0.15
        if star_size >= 6:
            grow = False
    else:
        star_size -= 0.15
        if star_size <= 2:
            star_size = 2
            grow = True
            star_index += 1
            if star_index > 2:
                star_index = 0

    # ---------------------------------
    # движение тарелки по синусоиде
    # ---------------------------------
    x = START_X + cur_pos
    y = CENTER_Y + sin(cur_pos * SPEED_WAVE) * AMPLITUDE

    # луч
    pygame.draw.polygon(
        screen,
        (255, 255, 120),
        [
            (x - 20, y + 20),
            (x + 20, y + 20),
            (x + 50, y + 100),
            (x - 50, y + 100)
        ]
    )

    # корпус тарелки
    pygame.draw.ellipse(screen, (160, 160, 170), (x - 60, y, 120, 35))

    # купол
    pygame.draw.ellipse(screen, (100, 220, 255), (x - 25, y - 20, 50, 30))

    cur_pos += step

    if x > 900:
        cur_pos = 0

    pygame.display.flip()
    clock.tick(60)
