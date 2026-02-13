
from functions import is_number

# Вариант 2

print('\nМодуль 3: Найти столбец, имеющий наименьшее количество отрицательных элементов.\n')

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

min_negative_count = matrix_rows # задаем за начальное значение длину столбца матрицы
ans_column = 0

for column in range(matrix_columns):
    curr_negative_count = 0
    for row in range(matrix_rows):
        if matrix[row][column] < 0:
            curr_negative_count += 1

    if curr_negative_count < min_negative_count:
        min_negative_count = curr_negative_count
        ans_column = column

print('\nСтолбец, имеющий наименьшее количество отрицательных элементов:', end = ' ')
for row_el in range(matrix_rows):
    print(matrix[row_el][ans_column], end = ' ')