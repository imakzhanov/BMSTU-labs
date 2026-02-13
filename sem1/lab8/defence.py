

# Ввод матрицы
matrix = []
matrix_side = int(input('Введите сторону матрицы: '))
if matrix_side <= 0:
    exit('Пустая матрица')

for i in range(matrix_side):
    matrix.append([])
    for j in range(matrix_side):
        el = input('Введите {}-й элемент {}-й строки: '.format(j+1, i+1))
        matrix[i].append(int(el))

#вывод исходной матрицы
for i in range(matrix_side):
    for j in range(matrix_side):
        print(f'{matrix[i][j]:^6}', end = '')
    print()

row = int(input('Введите номер строки(начиная с 1): '))
column = int(input('Введите номер столбца(начиная с 1): '))

# решение
per_el = matrix[row-1][column-1]

for i in range(matrix_side):
    if i == max(row - 1, column - 1): # пересечение заданной строки и столбца
        if row > column:
            matrix[row - 1][i], matrix[i][column - 1] = per_el, matrix[i][column - 1]
        else:
            matrix[row - 1][i], matrix[i][column - 1] = matrix[i][column - 1], per_el
    else:
        matrix[row - 1][i], matrix[i][column - 1] = matrix[i][column - 1], matrix[row - 1][i]

#вывод измененной матрицы
for i in range(matrix_side):
    for j in range(matrix_side):
        print(f'{matrix[i][j]:^6}', end = '')
    print()