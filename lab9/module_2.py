
from functions import *

print('\nМодуль 2: Поворот матрицы на 90 градусов\n')

# Ввод матрицы
matrix = []

matrix_side = int(input('Введите сторону матрицы: '))
if matrix_side <= 0:
    exit('Пустая матрица')

# Добавление в матрицу A
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
matrix_print(matrix, matrix_side, matrix_side)

# Поворот на 90 градусов по часовой стрелке
for i in range(matrix_side // 2):
    for j in range(i, matrix_side - (i + 1)):
        temp = matrix[i][j]

        matrix[i][j] = matrix[matrix_side - (j + 1)][i]
        matrix[matrix_side - (j + 1)][i] = matrix[matrix_side - (i + 1)][matrix_side - (j + 1)]
        matrix[matrix_side - (i + 1)][matrix_side - (j + 1)] = matrix[j][matrix_side - (i + 1)]
        matrix[j][matrix_side - (i + 1)] = temp
        matrix[j][matrix_side - (i + 1)] = temp

# Вывод повернутой матрицы
print('\nПовернутая по часовой стрелке матрица: ')
matrix_print(matrix, matrix_side, matrix_side)

#Против часовой на 90 градусов
for i in range(matrix_side // 2):
    for j in range(i, matrix_side - (i + 1)):
        temp = matrix[i][j]

        matrix[i][j] = matrix[j][matrix_side - (i + 1)]
        matrix[j][matrix_side - (i + 1)] = matrix[matrix_side - (i + 1)][matrix_side - (j + 1)]
        matrix[matrix_side - (i + 1)][matrix_side - (j + 1)] = matrix[matrix_side - (j + 1)][i]
        matrix[matrix_side - (j + 1)][i] = temp

# Вывод итоговой матрицы
print('\nИтоговая матрица: ')
matrix_print(matrix, matrix_side, matrix_side)
