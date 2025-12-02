
from functions import is_number

print('\nМодуль 6: транспонирование квадратной матрицы\n')

# Ввод матрицы
matrix = []
matrix_side = int(input('Введите сторону матрицы: '))
if matrix_side <= 0:
    exit('Пустая матрица')

for i in range(matrix_side):
    matrix.append([])
    for j in range(matrix_side):
        el = input('Введите {}-й элемент {}-й строки: '.format(j+1, i+1))
        if is_number(el):
            matrix[i].append(int(el))
        else:
            exit('Введено не число')

# Вывод исходной матрицы
print('\nИсходная матрица: ')
for i in range(matrix_side):
    for j in range(matrix_side):
        print(f'{matrix[i][j]:^6}', end=' ')
    print()

# Транспонирование
for i in range(matrix_side):
    for j in range(i):
        matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]

# Вывод измененной матрицы
print('\nТранспонированная матрица: ')
for i in range(matrix_side):
    for j in range(matrix_side):
        print(f'{matrix[i][j]:^6}', end=' ')
    print()

