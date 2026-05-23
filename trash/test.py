import pygame
import sys
from math import sin, cos, pi

x_circle = 400
y_circle = 300

def matr(x, y, time, x_center, y_center):
    time = time * 5.43
    x = x - x_center
    y = y - y_center
    m = [[sin(time/180), cos(time/180)],
         [-cos(time/180), sin(time/180)]]
    return x * m[0][0] + y*m[0][1] + x_center, x * m[1][0] + y*m[1][1] + y_center

def draw_triangle(x, y, time):
    rad = 30
    #def points
    ax, ay = x, y - rad
    bx, by = x - sin(pi/3)*rad, y + cos(pi/3)*rad
    cx, cy = x + sin(pi/3)*rad, y + cos(pi/3)*rad

    ax, ay = matr(ax, ay, time, x,y)
    bx, by = matr(bx, by, time, x,y)
    cx, cy = matr(cx, cy, time, x,y)

    a_triangle = [(x, y), (ax, ay), (bx, by)]
    b_triangle = [(x, y), (cx, cy), (bx, by)]
    c_triangle = [(x, y), (ax, ay), (cx, cy)]

    pygame.draw.polygon(screen, (255, 0, 0), a_triangle)
    pygame.draw.polygon(screen, (0, 255, 0), b_triangle)
    pygame.draw.polygon(screen, (0, 0, 255), c_triangle)


screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()


speed = 2
x_direction = -1 # -1 - left; 1 - right
radius = 200

x_triangle = 400
y_triangle = y_circle + radius

screen.fill((255, 255, 255))
pygame.draw.circle(screen, (0, 0, 0), (x_circle, y_circle), radius)
pygame.draw.circle(screen, (255, 255, 255), (x_circle, y_circle), radius - 3)

x_1 = [i for i in range(x_circle, x_circle - radius, -speed)]
y_1 = [-1*(radius ** 2 - (x - x_circle) ** 2) ** 0.5 + y_circle for x in x_1]
x_2 = [i for i in range(x_circle - radius, x_circle, speed)]
y_2 = [(radius ** 2 - (x - x_circle) ** 2) ** 0.5 + y_circle for x in x_2]
x_3 = [i for i in range(x_circle, x_circle + radius, speed)]
y_3 = [(radius ** 2 - (x - x_circle) ** 2) ** 0.5 + y_circle for x in x_3]
x_4 = [i for i in range(x_circle + radius, x_circle, -speed)]
y_4 = [-1*(radius ** 2 - (x - x_circle) ** 2) ** 0.5 + y_circle for x in x_4]

x_es = x_1 + x_2 + x_3 + x_4
y_es = y_1 + y_2 + y_3 + y_4

for i in range(len(x_es)):
    x, y = x_es[i], y_es[i]

    screen.fill((255, 255, 255))
    pygame.draw.circle(screen, (0, 0, 0), (x_circle, y_circle), radius, 3)
    draw_triangle(x, y, i)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()