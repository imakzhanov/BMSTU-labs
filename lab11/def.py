
"""
метод трапеций
"""
from functions import *


def f(x):  # Заданная функция
    try:
        value = x ** 2
        if type(value) == complex:
            return False
        return value
    except ArithmeticError:
        return False


def anti_f(x):  # Первообразная заданной функции
    try:
        value = (1/3) * x**3
        if type(value) == complex:
            return False
        return value
    except ArithmeticError:
        return False


def trapezoid_method(f, x_start, x_end, n):  # метод трапеций
    s = 0
    x_step = (x_end - x_start) / n
    for i in range(n):
        x_value = x_start + i * x_step
        s += (f(x_value) + f(x_value + x_step)) / 2 * x_step
    return s

# Ввод данных
while True:
    x_start = input('\nВведите начало отрезка интегрирования: ')
    x_end = input('\nВведите конец отрезка интергрирования: ')
    if not is_num(x_start) or not is_num(x_end):
        print('\nВведены не числа, повторите ввод')
    else:
        x_start = float(x_start)
        x_end = float(x_end)
        break

while True:
    n1 = input('\nВведите первое количество участков разбиения: ')
    n2 = input('\nВвежите второе количество участков разбиения: ')
    if not is_int(n1) or not is_int(n2):
        print('\nВведены не числа, повторите ввод')
    else:
        n1 = int(n1)
        n2 = int(n2)
        break



# Построение таблицы и погрешности

faults = []  # матрица погрешностей
real_value = round(anti_f(x_end) - anti_f(x_start), 9)  # реальное значение по первообразной

print('-' * 74)
print(f'|{' ':^30}|{n1:^20}|{n2:^20}|')
print('-' * 74)

print(f'|{'Метод трапеций':^30}|', end = '')
for n in [n1, n2]:
    value = median_rectangle_method(f, x_start, x_end, n)
    faults.append((abs(real_value - value),
                            abs(real_value - value) / real_value * 100))  # добавляем отн. и абс. погрешности
    print(f'{value:^20}|', end = '')
print()
print('-' * 74)

# вывод погрешностей

print(f'\n{'ПОГРЕШНОСТИ':^92}')
print(f'{' ':^30}|{n1:^30}|{n2:^30}')
print(f'{' ':^30}|{'Абсолютная':^15}{'Относительная,%':^15}|{'Абсолютная':^15}{'Относительная,%':^15}')
absolute, relavite = faults[0]
print(f'{' ':^30}|{absolute:^15.6f}{relavite:^15.6f}|', end = '')
absolute, relavite = faults[1]
print(f'{absolute:^15.6f}{relavite:^15.6f}', end = '')