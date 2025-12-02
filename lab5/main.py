
'''
Лабораторная работа 5, вариант 36
Макжанов Илья Игоревич ИУ7-16Б
Программа для построения графика функций
'''

# Ввод данных
while True:
    x_start = float(input('Введите начальное значение аргумента: '))
    x_step = float(input('Введите шаг: ')) # шаг для оси OX
    x_end = float(input('Введите конечное значение аргумента: '))
    if x_start <= x_end and x_step > 0:
        break
    else:
        print('Значения введены некорректно, повторите ввод(Z0 < Z1, шаг > 0)')

# Количество точек, по которым строится график и таблица
points_amount = int(round(((x_end - x_start) / x_step), 9)) + 1

# Шапка таблицы
print('-'*33,
      f'|{'X':^15}|{'F(X)':^15}|',
      '-'*33, sep = '\n')

# Мин и макс значения функции на данном интервале (для построения графика)
min_value = (x_start ** 9 + 3 * x_start ** 8 - x_start ** 7
            + x_start ** 6 + 6 * x_start ** 5 - 7 * x_start ** 4 + x_start ** 3
             + x_start ** 2 - x_start + 2)
max_value = (x_end ** 9 + 3 * x_end ** 8 - x_end ** 7
            + x_end ** 6 + 6 * x_end ** 5 - 7 * x_end ** 4 + x_end ** 3
             + x_end ** 2 - x_end + 2)
x_max = x_end # точка максимума функции

# Вывод таблицы
for i in range(points_amount):
    x_value = round(x_start + i * x_step, 9) # аргумент
    function_value = (x_value ** 9 + 3 * x_value ** 8 - x_value ** 7
            + x_value ** 6 + 6 * x_value ** 5 - 7 * x_value ** 4 + x_value ** 3
             + x_value ** 2 - x_value + 2) # Значение функции
    min_value = min(min_value, function_value)
    if function_value > max_value:
        max_value = function_value
        x_max = x_value
    print(f'|{x_value:^15.7g}|{function_value:^15.7g}|')
print('-'*33)


serifs = int(input('\nВведите число засечек (от 4 до 8, целое число): '))
# Фиксированная область печати графика - 100 символов
axis_step = (max_value - min_value) / (serifs - 1) # шаг для оси OY

# Построение оси OY
last_len = 0
print(f'\n{'x\\y':^15}|', end = '')
for i in range(serifs):
    axis_value = round(min_value + i * axis_step, 3)  # значение функции для оси OY
    point_position = int((axis_value - min_value) * 100 // (max_value - min_value))
    print(' ' * (point_position - last_len) + f'{axis_value}', end = '')
    last_len = len(str(axis_value)) + point_position
print()

# Построение графика
for i in range(points_amount):
    x_value = round(x_start + i * x_step, 9)
    function_value = (x_value ** 9 + 3 * x_value ** 8 - x_value ** 7
            + x_value ** 6 + 6 * x_value ** 5 - 7 * x_value ** 4 + x_value ** 3
             + x_value ** 2 - x_value + 2)
    point_position = int((function_value - min_value) * 100 // (max_value - min_value))

    # Вывод параметра x
    print(f'{x_value:^15.7g}|', end = '')

    if min_value <= 0 <= max_value: # 0 находится в отрезке значений функции
        zero_position = int(-min_value * 100 // (max_value - min_value))

        if point_position < zero_position:
            print(' '*point_position + '*' + ' '*(zero_position - point_position - 1) + '|')
        elif point_position == zero_position:
            print(' '*point_position + '*')
        else:
            print(' ' * zero_position + '|' + ' ' * (point_position - zero_position - 1) + '*')

    else: # 0 не входит в отрезок значений функции
        print(' '*point_position + '*')

print(f'\nМаксимальное значение функции на отрезке = {max_value}, достигается при x = {x_max}')
