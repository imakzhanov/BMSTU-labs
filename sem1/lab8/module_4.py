
from functions import is_number

print('\nМодуль 4: Переставить местами столбцы с максимальной и минимальной суммой элементов\n')


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


max_index, max_sum_value = 0, float('-inf')
min_index, min_sum_value = 0, float('inf')

for column in range(matrix_columns):
    summ = 0
    for row_inx in range(matrix_rows):
        summ += matrix[row_inx][column]

    if summ > max_sum_value:
        max_sum_value = summ
        max_index = column
    elif summ < min_sum_value:
        min_sum_value = summ
        min_index = column

# Меняем местами столбцы
for row in range(matrix_rows):
    matrix[row][max_index], matrix[row][min_index] = matrix[row][min_index], matrix[row][max_index]

# Вывод измененной матрицы
print('\nИзмененная матрица: ')
for i in range(matrix_rows):
    for j in range(matrix_columns):
        print(f'{matrix[i][j]:^6}', end=' ')
    print()
