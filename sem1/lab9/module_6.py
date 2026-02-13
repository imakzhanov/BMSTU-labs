
from functions import matrix_print

print('\nМодуль 6: \n')

# Ввод матрицы
matrix = []

matrix_rows = int(input('Введите количество строк в матрице: '))
matrix_columns = int(input('Введите количество cтолбцов в матрице: '))
if matrix_rows <= 0 or  matrix_columns <= 0:
    exit('Пустая матрица')

for i in range(matrix_rows):
    matrix.append([])
    for j in range(matrix_columns):
        el = input('Введите {}-й элемент {}-й строки: '.format(j+1, i+1))
        if len(el) == 1:
            matrix[i].append(el)
        else:
            exit('Введен не символ')

# Вывод исходной матрицы
print('\nВведенная матрица: ')
matrix_print(matrix, matrix_rows, matrix_columns)

# Решение
consonants = 'bcdfghjklmnpqrstvwxz'
vowels = 'AEIOUY'

for i in range(matrix_rows):
    for j in range(matrix_columns):
        if matrix[i][j] in consonants:
            matrix[i][j] = matrix[i][j].upper()
        elif matrix[i][j] in vowels:
            matrix[i][j] = matrix[i][j].lower()

# Вывод матрицы
print('\nПолученная матрица: ')
matrix_print(matrix, matrix_rows, matrix_columns)
