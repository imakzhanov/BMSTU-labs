"""
Макжанов Илья ИУ7-26Б
Из заданного множества точек на плоскости выбрать две
различные точки так, чтобы окружности заданного радиуса
с центрами в этих точках содержали внутри себя
одинаковое количество заданных точек.
"""

from math import *

def is_in_triangle(point_to_check, point, radius):
    x, y = point
    a = (x + radius * cos(radians(90)), y + radius * sin(radians(90)))
    b = (x + radius * cos(radians(210)), y + radius * sin(radians(210)))
    c = (x + radius * cos(radians(330)), y + radius * sin(radians(330)))

    def cross(p1, p2, p3):
        return (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0])

    c1 = cross(a, b, point_to_check)
    c2 = cross(b, c, point_to_check)
    c3 = cross(c, a, point_to_check)

    return (c1 >= 0 and c2 >= 0 and c3 >= 0) or (c1 <= 0 and c2 <= 0 and c3 <= 0)


# считает сколько точек лежат внутри окружности с центром в данной точке point и радиусом radius
def count_included_points(point: tuple[int, int], points: list[tuple[int, int]], radius: int) -> int:
    included_points = 0
    for cur_point in points:
        if is_in_triangle(cur_point, point, radius):
            included_points += 1

    return included_points


def find_points(points: list[tuple[int, int]], radius: int) -> tuple[tuple[int, int], tuple[int, int], int] | None:
    included_count = []
    for i in points:
        included_count.append(count_included_points(i, points, radius))

    for i in range(len(included_count)):
        for j in range(i + 1, len(included_count)):
            if included_count[i] == included_count[j]:
                return points[i], points[j], included_count[i]

    # точки не найдены
    return None

