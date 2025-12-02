from functions import *

print('\nМодуль 4: \n')

# Ввод матриц
matrix_d = []

matrix_rows = int(input('Введите количество строк в матрице: '))
matrix_columns = int(input('Введите количество cтолбцов в матрице: '))
if matrix_rows <= 0 or  matrix_columns <= 0:
    exit('Пустая матрица')

for i in range(matrix_rows):
    matrix_d.append([])
    for j in range(matrix_columns):
        el = input('Введите {}-й элемент {}-й строки: '.format(j+1, i+1))
        if is_number(el):
            matrix_d[i].append(int(el))
        else:
            exit('Введено не число')

list_l = list(map(int, input('Введите массив (числа через пробел): ').split()))

# Решение
list_r = []
list_r_middle = 0 # сред. значение максимальных элементов
for i in list_l:
    if i < 1 or i > matrix_rows:
        exit('Неверный номер строки')

    maxx = matrix_d[i-1][0] # поиск макс. элемента строки
    for j in range(matrix_columns):
        if matrix_d[i-1][j] > maxx:
            maxx = matrix_d[i-1][j]
    list_r.append(maxx)
    list_r_middle += maxx
list_r_middle /= len(list_r)

# Вывод значений
print('\nМатрица D: ')
matrix_print(matrix_d, matrix_rows, matrix_columns)

print('\nМассив L:', *list_l)
print('\nМассив R:', *list_r)
print(f'\nСред. арифм. массива R: {list_r_middle:.5g}')
