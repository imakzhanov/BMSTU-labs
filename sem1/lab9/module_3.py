
from functions import *

print('\nМодуль 3: \n')

# Ввод матриц
matrix_a = []
matrix_b = []

matrix_columns = int(input('Введите количество cтолбцов для обеих матриц: '))
matrix_rows_a = int(input('Введите количество строк в матрице A: '))
if matrix_rows_a <= 0 or  matrix_columns <= 0:
    exit('Пустая матрица')

# Добавление в матрицу A
for i in range(matrix_rows_a):
    matrix_a.append([])
    for j in range(matrix_columns):
        el = input('Введите {}-й элемент {}-й строки: '.format(j+1, i+1))
        if is_number(el):
            matrix_a[i].append(int(el))
        else:
            exit('Введено не число')

matrix_rows_b = int(input('Введите количество строк в матрице B: '))
if matrix_rows_b <= 0:
    exit('Пустая матрица')

# Добавление в матрицу B
for i in range(matrix_rows_b):
    matrix_b.append([])
    for j in range(matrix_columns):
        el = input('Введите {}-й элемент {}-й строки: '.format(j+1, i+1))
        if is_number(el):
            matrix_b[i].append(int(el))
        else:
            exit('Введено не число')

# Вывод исходных матриц
print('\nИсходная матрица A: ')
matrix_print(matrix_a, matrix_rows_a, matrix_columns)
print('\nИсходная матрица B: ')
matrix_print(matrix_b, matrix_rows_b, matrix_columns)


# решение
s = [] # список количества элементов, больших среднего арифметического соответствующего столбца матрицы В

for j in range(matrix_columns):
    column_middle = 0 # среднее арифм для столбца матрицы B
    for i in range(matrix_rows_b):
        column_middle += matrix_b[i][j]
    column_middle /= matrix_rows_b

    el_count = 0 # кол-во элементов для столбца
    for i in range(matrix_rows_a):
        if matrix_a[i][j] > column_middle:
            el_count += 1
    s.append(el_count)

    if column_middle != 0: # преобразрвание матрицы B
        for i in range(matrix_rows_b):
            matrix_b[i][j] *= column_middle


# вывод значений
print(f'\n{'Кол-во элементов, больших ср.арифм:':^40}|', end = '')
for i in range(matrix_columns):
    print(f'{s[i]:^6}', end = '')

print(f'\n\n{'Измененная матрица B: ':^40}|', end='')
for i in range(matrix_rows_b):
    for j in range(matrix_columns):
        print(f'{matrix_b[i][j]:^6.5g}', end='')
    print('\n' + ' '*40 + '|', end = '')