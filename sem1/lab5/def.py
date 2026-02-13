
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
        print('Значения введены некорректно, повторите ввод(x0 < x1, шаг > 0)')

# Мин и макс значения функции на данном интервале (для построения графика)
min_value = -(x_start**2) + 4
max_value = -(x_end**2) + 4
# Нахождение макс и мин значений функции на отрезке
x_value = x_start
while x_value <= x_end:
    function_value = -(x_value**2) + 4
    min_value = min(min_value, function_value)
    max_value = max(max_value, function_value)
    x_value = round(x_value + x_step, 9)

# Фиксированная область печати графика - 100 символов
# Построение оси OY
print(f'\n{'x\\y':^15}|', end = '')
print(f'{min_value}' + ' '*(100 - len(str(min_value))) + f'{max_value}')

# определение позиции для оси абцисс
if min_value <= 0 <= max_value:  # 0 находится в отрезке значений функции
    zero_position = int(-min_value * 100 // (max_value - min_value))

# Построение графика
x_value = x_start
while x_value <= x_end:
    function_value = -(x_value**2) + 4
    point_position = int((function_value - min_value) * 100 // (max_value - min_value))

    # Вывод параметра x
    print(f'{x_value:^15.7g}|', end = '')

    if min_value <= 0 <= max_value: # 0 находится в отрезке значений функции
        if point_position < zero_position:
            print(' '*point_position + '*' + ' '*(zero_position - point_position - 1) + '|')
        elif point_position == zero_position:
            print(' '*point_position + '*')
        else:
            print(' ' * zero_position + '|' + ' ' * (point_position - zero_position - 1) + '*')

    else: # 0 не входит в отрезок значений функции
        print(' '*point_position + '*')

    x_value = round(x_value + x_step, 9)