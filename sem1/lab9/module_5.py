from functions import *


print('\nМодуль 5: Умножение матриц\n')

# Ввод матриц
matrix_a = []
matrix_b = []

# Добавление в матрицу A
matrix_rows_a = int(input('Введите количество строк в матрице A: '))
matrix_columns_a = int(input('Введите количество cтолбцов для матрицы A: '))
if matrix_rows_a <= 0 or  matrix_columns_a <= 0:
    exit('Пустая матрица')

for i in range(matrix_rows_a):
    matrix_a.append([])
    for j in range(matrix_columns_a):
        el = input('Введите {}-й элемент {}-й строки: '.format(j+1, i+1))
        if is_number(el):
            matrix_a[i].append(int(el))
        else:
            exit('Введено не число')

# Добавление в матрицу B
matrix_rows_b = int(input('Введите количество строк в матрице B: '))
matrix_columns_b = int(input('Введите количество cтолбцов для матрицы B: '))
if matrix_rows_b <= 0 or  matrix_columns_b <= 0:
    exit('Пустая матрица')

for i in range(matrix_rows_b):
    matrix_b.append([])
    for j in range(matrix_columns_b):
        el = input('Введите {}-й элемент {}-й строки: '.format(j+1, i+1))
        if is_number(el):
            matrix_b[i].append(int(el))
        else:
            exit('Введено не число')


# Вывод исходных матриц
print('\nИсходная матрица A: ')
matrix_print(matrix_a, matrix_rows_a, matrix_columns_a)
print('\nИсходная матрица B: ')
matrix_print(matrix_b, matrix_rows_b, matrix_columns_b)

# Проверка на согласованность матриц
if matrix_columns_a != matrix_rows_b:
    exit('Невозможно умножить, число столбцов матрицы A не совпадает с числом строк матрицы B')

# Даны матрицы a*b и b*c, получается матрица a*c
# Решение
matrix_c = []
for i in range(matrix_rows_a):
    matrix_c.append([])
    for j in range(matrix_columns_b):
        el_value = 0
        for k in range(matrix_columns_a):
            el_value += matrix_a[i][k] * matrix_b[k][j]
        matrix_c[i].append(el_value)

# Вывод матрицы
print('\nМатрица С - результат умножения матриц А и В:')
matrix_print(matrix_c, matrix_rows_a, matrix_columns_b)

