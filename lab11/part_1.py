'''
Макжанов Илья Игоревич ИУ7-16Б
Лабораторная 11
Вычисление приближённого значения интеграла
метод срединных прямоугольников и метод 3/8
'''

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
for method in range(2):
    faults.append([])

    if method == 0:
        str_to_print = f'|{'Серединные прямоугольники':^30}|'
    else:
        str_to_print = f'|{'Метод Симпсона 3/8':^30}|'
    for n in [n1, n2]:
        if method == 0:
            value = median_rectangle_method(f, x_start, x_end, n)
            faults[method].append((abs(real_value - value),
                                   abs(real_value - value) / real_value * 100))  # добавляем отн. и абс. погрешности
            str_to_print += f'{value:^20}|'
        else:
            value = three_eight_method(f, x_start, x_end, n)
            if value:
                faults[method].append((abs(real_value - value),
                                       abs(real_value - value) / real_value * 100))  # добавляем отн. и абс. погрешности
                str_to_print += f'{value:^20}|'
            else:
                faults[method].append(('-', '-'))
                str_to_print += f'{'-':^20}|'
    print(str_to_print)
    print('-' * 74)

# вывод погрешностей

accurate_method_number = 0  # номер точного метода
min_fault = float('inf')  # минимальная погрешность

print(f'\n{'ПОГРЕШНОСТИ':^92}')
print(f'{' ':^30}|{n1:^30}|{n2:^30}')
print(f'{' ':^30}|{'Абсолютная':^15}{'Относительная,%':^15}|{'Абсолютная':^15}{'Относительная,%':^15}')
for method in range(len(faults)):
    if method == 0:
        str_to_print = f'{'Серединные прямоугольники':^30}'
    else:
        str_to_print = f'{'Метод Симпсона 3/8':^30}'
    for n in range(len(faults[method])):
        absolute, relative = faults[method][n]
        if absolute != '-':
            str_to_print += f'|{absolute:^15.6f}{relative:^15.6f}'

            if absolute < min_fault:
                min_fault = absolute
                if method == 0:
                    accurate_method_number = 0
                else:
                    accurate_method_number = 1
        else:
            str_to_print += f'|{'-':^15}{'-':^15}'

    print(str_to_print)

# точный метод
if accurate_method_number == 0:
    print('\nСамый точный метод: Серединные прямоугольники')
else:
    print('\nСамый точный метод: Метод Симпсона 3/8')

# Вычисление участков разбиения по заданной точности

while True:
    eps = input('\nВведите точность E: ')
    if is_num(eps):
        eps = float(eps)
        break
    else:
        print('\nВведено не число, повторите ввод')

if accurate_method_number == 0:  # поиск N для метода 3/8
    n = 3
    while abs(three_eight_method(f, x_start, x_end, n) - three_eight_method(f, x_start, x_end, 2 * n)) >= eps:
        n += 3
    print(f'\nКол-во участков для вычисления с точностью {eps} методом 3/8 = {n}, '
          f'полученное значение интеграла при данном n = {three_eight_method(f, x_start, x_end, n)}')

else:  # поиск N для метода серединных прямоугльников
    n = 1
    while abs(median_rectangle_method(f, x_start, x_end, n) - median_rectangle_method(f, x_start, x_end, 2 * n)) >= eps:
        n += 1
    print(f'\nКол-во участков для вычисления с точностью {eps} методом серединных прямоугольников = {n}, '
          f'полученное значение интеграла при данном n = {median_rectangle_method(f, x_start, x_end, n)}')
