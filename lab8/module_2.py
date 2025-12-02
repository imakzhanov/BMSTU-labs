
from functions import is_number

print('\nМодуль 2: Переставить местами строки с наибольшим и наименьшим количеством отрицательных элементов\n')

# Ввод матрицы
matrix = []
matrix_columns = int(input('Введите количество cтолбцов в матрице: '))
matrix_rows = int(input('Введите количество строк в матрице: '))
if matrix_rows <= 0 or  matrix_columns <= 0:
    exit('Пустая матрица')

for i in range(matrix_rows):
    matrix.append([])
    for j in range(matrix_columns):
        el = input('Введите {}-й элемент {}-й строки: '.format(j+1, i+1))
        if is_number(el):
            matrix[i].append(int(el))
        else:
            exit('Введено не число')

# Вывод исходной матрицы
print('\nИсходная матрица: ')
for i in range(matrix_rows):
    for j in range(matrix_columns):
        print(f'{matrix[i][j]:^6}', end=' ')
    print()

# Решение
max_index, max_negative_count = 0, 0
min_index, min_negative_count = 0, matrix_columns # задаем за начальное значение длину строки

for row in range(matrix_rows):
    curr_negative_count = 0
    for j in matrix[row]:
        if j < 0:
            curr_negative_count += 1

    if curr_negative_count > max_negative_count:
        max_negative_count = curr_negative_count
        max_index = row
    elif curr_negative_count < min_negative_count:
        min_negative_count = curr_negative_count
        min_index = row

# Меняем местами строки
matrix[max_index], matrix[min_index] = matrix[min_index], matrix[max_index]

# Вывод полученной матрицы
print('\nИзмененная матрица: ')
for i in range(matrix_rows):
    for j in range(matrix_columns):
        print(f'{matrix[i][j]:^6}', end=' ')
    print()