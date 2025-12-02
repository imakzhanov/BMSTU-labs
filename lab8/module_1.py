
from functions import is_number

# Вариант 3

print('\nМодуль 1: Найти строку в матрице, имеющую наибольшее количество четных элементов\n')

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
ans_index = 0
max_even_count = 0
for row in range(matrix_rows):
    current_even_count = 0
    for j in matrix[row]:
        if abs(j) % 2 == 0:
            current_even_count += 1
    if current_even_count > max_even_count:
        max_even_count = current_even_count
        ans_index = row

print('Строка с максимальным количеством четных элементов:', *matrix[ans_index])
