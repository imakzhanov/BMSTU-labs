from functions import *
from math import sin, cos

def f(x):
    try:
        value = sin( x/2)
        if type(value) == complex:
            return False
        return value
    except ArithmeticError:
        return False


def g(x):
    try:
        value = cos(x/2)
        if type(value) == complex:
            return False
        return value
    except ZeroDivisionError:
        return False


def y(x):
    if f(x) and g(x):
        return f(x) - g(x)
    return False


def find_zeros(f):  # поиск точек пересечения функций
    interval = [-20, 20]
    step = 1
    eps = 1e-3

    def half_division(f, a, b, eps):
        if f(a) and f(b):
            if f(a) * f(b) > 0:  # нет корней на интервале
                return False

            for _ in range(100):  # макс. количество итераций
                c = (a + b) / 2
                if abs(f(c)) < eps:  # корень найден
                    return c
                if f(a) * f(c) < 0:
                    b = c
                else:
                    a = c
            return c

        else:
            return False

    a, b = interval
    zeros = []
    x = a
    while x < b:
        zero = half_division(f, x, x + step, eps)
        if zero is not False and abs(f(zero)) < eps:
            for i in zeros:  # Проверяем на повторение
                if abs(zero - i) < eps:
                    break  # повторение
            else:
                zeros.append(zero)
        x += step

    if len(zeros) < 2:
        return False
    return zeros[:2]  # позвращаем первые 2 точки


# ввод точности eps
while True:
    eps = input('\nВведите точность (eps): ')
    if is_num(eps):
        eps = float(eps)
        break
    else:
        print('\nВведено не число, повторите ввод')


zeros = find_zeros(y) # точки пересечения функций
if zeros:
    x_start = zeros[0]
    x_end = zeros[1]
    n = 3
    while abs(three_eight_method(y, x_start, x_end, n) - three_eight_method(y, x_start, x_end, 2 * n)) >= eps:
        n += 3
    print(f'\nПлощадь замкнутой фигуры с точностью {eps} = {abs(three_eight_method(y, x_start, x_end, n))}')
else:
    print('\nФункции имеют меньше 2 точек пересечения на заданном интервале')

# построение графика
WIDTH = 90  # ширина печати графика

x_start = -16
x_end = -10
x_steps = 20  # количество точек на графиках
x_step_value = (x_end - x_start) / x_steps

# подсчет оси OY
min_y_value = min(f(x_start), g(x_start))
max_y_value = max(f(x_end), g(x_end))

x_value = x_start
# поиск максимумов и минмумов на интервале
while x_value < x_end:
    min_y_value = min(f(x_value), g(x_value), min_y_value)
    max_y_value = max(f(x_value), g(x_value), max_y_value)
    x_value += x_step_value

# вывод засечек

y_steps = 10  # количество засечек
y_step_value = (max_y_value - min_y_value) / (y_steps - 1)
last_len = 0
print(f'\n{'x\\y':^15}|', end='')
for i in range(y_steps):
    y_value = round(min_y_value + i * y_step_value, 5)
    serif_position = int((y_value - min_y_value) * WIDTH // (max_y_value - min_y_value))
    print(' ' * (serif_position - last_len) + f'{y_value}', end='')
    last_len = len(str(y_value)) + serif_position
print()

# Построение графика

x_value = x_start
while x_value <= x_end:
    line = [' '] * (WIDTH + 1)
    # Подсчет позиций для точек
    if min_y_value <= 0 <= max_y_value:
        zero_position = int((-min_y_value) * WIDTH / (max_y_value - min_y_value))
        line[zero_position] = '|'

    if type(f(x_value)) != bool:
        f_position = int((f(x_value) - min_y_value) * WIDTH / (max_y_value - min_y_value))
        line[f_position] = 'F'

    if type(g(x_value)) != bool:
        g_position = int((g(x_value) - min_y_value) * WIDTH / (max_y_value - min_y_value))
        line[g_position] = 'G'


    # закрашенная область (область пересечения)
    if zeros:
        if zeros[0] < x_value < zeros[1]:
            if f_position > g_position:
                for i in range(g_position + 1, f_position):
                    line[i] = '░'
            else:
                for i in range(f_position + 1, g_position):
                    line[i] = '░'

    print(f'{x_value:^15.1f}|' + ''.join(line))

    x_value += x_step_value

