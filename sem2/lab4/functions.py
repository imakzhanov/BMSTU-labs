"""
Макжанов Илья ИУ7-26Б
Из заданного множества точек на плоскости выбрать две
различные точки так, чтобы окружности заданного радиуса
с центрами в этих точках содержали внутри себя
одинаковое количество заданных точек.
"""

import math

def calc_distance(a: tuple[int, int], b: tuple[int, int]) -> float:
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)


def count_included_points(point: tuple[int, int], points: list[tuple[int, int]], radius: int) -> int:
    "считает сколько точек лежат внутри окружности с центром в данной точке point и радиусом radius"
    included_points = 0
    for cur_point in points:
        if calc_distance(point, cur_point) < radius:
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

