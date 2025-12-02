
from functions import is_number

print('\nМодуль 5: Найти максимальное значение в квадратной матрице над главной диагональю и '
      'минимальное - под побочной диагональю\n')

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

max_value = float('-inf')
min_value = float('inf')
is_exists = False

#Поиск максимального над главной диагональю
for i in range(matrix_side - 1):
    for j in range(i + 1, matrix_side):
        if not is_exists: # Проверка на существование такого числа
            is_exists = True
        max_value = max(max_value, matrix[i][j])

# Поиск минимального под побочной диагональю
for i in range(1, matrix_side):
    for j in range(matrix_side - i, matrix_side):
        min_value = min(min_value, matrix[i][j])

if is_exists:
    print(f'\nМаксимальное значение над главной диагональю: {max_value}')
    print(f'Минимальное значение под побочной диагональю: {min_value}')
else:
    print('\nЭлементов над главной и под побочной не существует')