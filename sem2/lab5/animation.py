import pygame
import sys
from math import sin, cos, pi
from random import randint


# рисует закрашенный полукруг
def draw_half_circle(surface, color, center, radius, segments=50):
    points = [center]

    for i in range(segments + 1):
        angle = pi * i / segments
        x = center[0] + radius * cos(angle)
        y = center[1] + radius * sin(angle)
        points.append((x, y))
    pygame.draw.polygon(surface, color, points)


def draw_cabin(x, y, angle, color):
    CABIN_RADIUS = 40
    ROPE_LEN = 70

    pygame.draw.circle(screen, BLACK, (x, y), 7)
    x_cabin, y_cabin = x + ROPE_LEN * cos(angle), y + ROPE_LEN * sin(angle)
    pygame.draw.line(screen, BLACK, (x, y), (x_cabin, y_cabin), 5)
    # рисуем кабинку
    draw_half_circle(screen, color, (x_cabin, y_cabin), CABIN_RADIUS)

# основная фукнция, которая рисует колесо обозрения
def draw_wheel(x, y, angle, cabins_colors):
    NEEDLES_COUNT = 5
    needle_angle = 0
    # спицы колеса
    while needle_angle < pi:
        x_start, x_end = x + RADIUS * cos(needle_angle + angle), x + RADIUS * cos(needle_angle + pi + angle)
        y_start, y_end = y + RADIUS * sin(needle_angle + angle), y + RADIUS * sin(needle_angle + pi + angle)
        pygame.draw.line(screen, BLACK, (x_start, y_start), (x_end, y_end), 5)
        needle_angle += pi / NEEDLES_COUNT
    pygame.draw.circle(screen, BLACK, (x, y), RADIUS, 5)
    pygame.draw.line(screen, BLACK, (x, y), (250, 720), 15)
    pygame.draw.line(screen, BLACK, (x, y), (550, 720), 15)

    # кабинки
    for cabin_number in range(CABINS_COUNT):
        cabin_angle = cabin_number / CABINS_COUNT * 2 * pi
        x_cabin = x + RADIUS * cos(cabin_angle + angle)
        y_cabin = y + RADIUS * sin(cabin_angle + angle)
        cabin_shake_angle = pi / 2 + MAX_ANGLE * sin(angle * 10)

        draw_cabin(x_cabin, y_cabin, cabin_shake_angle, cabins_colors[cabin_number])


# Цвета
BLACK = (0, 0, 0)
SKY_BLUE = (135, 206, 235)
GRASS_GREEN = (34, 139, 34)
SUN_YELLOW = (255, 255, 0)

# константы
RADIUS = 200
SPEED = 0.003
CABINS_COUNT = 7
MAX_ANGLE = 0.7

SUN_RADIUS = 150
SUN_SHIFT = 20

# Настройка окна
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

X_CENTER = WIDTH // 2
Y_CENTER = HEIGHT // 2

angle = 0
sun_size = SUN_RADIUS

# список цветов кабинок
cabins_colors = [(randint(0, 255), randint(0, 255), randint(0, 255)) for _ in range(CABINS_COUNT)]

# создание звука
pygame.mixer.init()
pygame.mixer.music.load("music.mp3")
pygame.mixer.music.play(-1)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # фон
    screen.fill(SKY_BLUE)
    pygame.draw.rect(screen, GRASS_GREEN, (0, 500, WIDTH, HEIGHT - 500))
    pygame.draw.circle(screen, SUN_YELLOW, (0, 0), sun_size)

    draw_wheel(X_CENTER, Y_CENTER, angle, cabins_colors)


    # изменение размера солнца и угла поворота колеса
    angle += SPEED
    sun_size = SUN_RADIUS + SUN_SHIFT * sin(angle * 5)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
