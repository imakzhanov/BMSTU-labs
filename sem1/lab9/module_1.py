
from math import sqrt

print('\nМодуль 2: Формирование матрицы из 2 списков\n')

# Ввод данных

a = list(map(int, input('Введите массив A (числа через пробел): ').split()))
b = list(map(int, input('Введите массив B (числа через пробел): ').split()))

# Решение
matrix = []
s = []

for i in range(len(a)):
    matrix.append([])
    square_counter = 0 # счетчик полных квадратов
    for j in range(len(b)):
        matrix_el = a[i] * b[j]
        matrix[i].append(matrix_el)
        if sqrt(matrix_el) == int(sqrt(matrix_el)):
            square_counter += 1
    s.append(square_counter)

# Вывод матрицы
print(f'\n{'Количество полных квадратов:':^30}|{'Полученная матрица: ':^30}')
for i in range(len(a)):
    print(f'{s[i]:^30}|', end = '') # Вывод кол-ва полных квадратов
    for j in range(len(b)):
        print(f'{matrix[i][j]:^8}', end='')
    print()

