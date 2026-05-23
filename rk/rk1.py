import math

import pygame
from math import sin, cos, pi


def draw_triangle(x, y):
    angles = [3 * pi / 2, 5 * pi / 6, pi / 6]

    # поворачиваем на angle / 2
    ax, ay = x + cos(angles[0] + angle * 2) * TRIANGLE_SIDE, y + sin(angles[0] + angle * 2) * TRIANGLE_SIDE
    bx, by = x + cos(angles[1] + angle * 2) * TRIANGLE_SIDE, y + sin(angles[1] + angle * 2) * TRIANGLE_SIDE
    cx, cy = x + cos(angles[2] + angle * 2) * TRIANGLE_SIDE, y + sin(angles[2] + angle * 2) * TRIANGLE_SIDE

    a_triangle = [(ax, ay), (bx, by), (x, y)]
    b_triangle = [(cx, cy), (bx, by), (x, y)]
    c_triangle = [(ax, ay), (cx, cy), (x, y)]

    pygame.draw.polygon(screen, RED, a_triangle)
    pygame.draw.polygon(screen, GREEN, b_triangle)
    pygame.draw.polygon(screen, BLUE, c_triangle)


# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

x_center = 500
y_center = 500

RADIUS = 300
TRIANGLE_SIDE = 60
SPEED = pi / 250

screen = pygame.display.set_mode((1000, 1000))
clock = pygame.time.Clock()

angle = 3 * pi / 2

processing = True
while processing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            processing = False

    screen.fill(WHITE)
    pygame.draw.circle(screen, BLACK, (x_center, y_center), RADIUS, 3)

    x_pos = x_center + RADIUS * cos(angle)
    y_pos = y_center + RADIUS * sin(angle)

    draw_triangle(x_pos, y_pos)

    angle += SPEED
    if angle >= 3 * pi / 2 + 2 * pi:
        processing = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
