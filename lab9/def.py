
"""
вариант 2
"""

def def_matrix(n,m):
    return [[i * m + j + 1 for j in range(m)] for i in range(n)]

n = int(input('Введите N (от 3 до 10): '))
m = int(input('Введите M (от 3 до 10): '))
matrix = def_matrix(n,m)
'''
for i in range(n):
    matrix.append([])
    for j in range(m):
        matrix[i].append(int(input(f'Введите {j + 1} элемент {i + 1} строки: ')))
'''

# вывод матрицы
for i in range(n):
    for j in range(m):
        print(f'{matrix[i][j]:^6}', end='')
    print()

a,b,c = map(int, input('Введите 3 числа через пробел: ').split())

first_const = None
second_const = None
f = True
counter = 0

for i in range(n):
    for j in range(m):
        if matrix[i][j] in [a,b,c]:
            counter += 1
            if first_const is None and second_const is None:
                first_const = i - j
                second_const = i + j
            elif f:
                if i - j == first_const:
                    second_const = None
                elif i + j == second_const:
                    first_const = None
                else:
                    f = False
                    break
    if not f:
        break


if counter != 3:
    print('\nне все числа есть в матрице')
else:
    if f:
        print('\nлежат на одной диагонали')
    else:
        print('\nне лежат на одной диагонали')
