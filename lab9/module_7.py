
from functions import is_number

print('\nМодуль 7: Трехмерный массив\n')

# Ввод данных
matrix = []

len_x = int(input('Введите длину массива по X(глубина): '))
len_y = int(input('Введите длину массива по Y(количество строк): '))
len_z = int(input('Введите длину массива по Z(количество столбцов): '))
if len_x <= 0 or len_y <= 0 or len_z <= 0:
    exit('Пустая матрица')

for x in range(len_x):
    matrix.append([])
    for y in range(len_y):
        matrix[x].append([])
        for z in range(len_z):
            el = input('Введите элемент с коорд. X = {} | Y = {} | Z = {}: '.format(x + 1, y + 1, z + 1))
            if is_number(el):
                matrix[x][y].append(int(el))
            else:
                exit('Введено не число')

# решение
if len_x >= max(len_y, len_z): # наибольшее измерение - X
    print(f'\nНаибольшее измерение X, срез по X = {len_x//2 + 1}: ')
    for y in range(len_y):
        for z in range(len_z):
            print(f'{matrix[len_x//2][y][z]:^6}', end = '')
        print()

elif len_y >= max(len_x, len_z): # наибольшее измерение - Y
    print(f'\nНаибольшее измерение Y, срез по Y = {len_y//2 + 1}: ')
    for x in range(len_x):
        for z in range(len_z):
            print(f'{matrix[x][len_y//2][z]:^6}', end = '')
        print()

else: # наибольшее измерение - Z
    print(f'\nНаибольшее измерение Z:, срез по Z = {len_z//2 + 1} ')
    for x in range(len_x):
        for y in range(len_y):
            print(f'{matrix[x][y][len_z//2]:^6}' , end = '')
        print()
