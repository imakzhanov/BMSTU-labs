
'''
Макжанов Илья Игоревич ИУ7-16Б
Задание 5, вариант 5
'''

print('\nМодуль 5, поменять местами минимальный чётный и максимальный нечётный элементы')
sp = list(map(int, input('\nВведите список (числа через пробел): ').split()))

max_odd, min_even = float('-inf'), float('+inf')
max_odd_index, min_even_index = 0, 0

odd_exists = False # существует ли нечетный элемент
even_exists = False # сущестует ли четный элемент

for i in range(len(sp)):
    if sp[i] % 2 == 0 and sp[i] < min_even:
        min_even = sp[i]
        min_even_index = i
        even_exists = True
    if sp[i] % 2 == 1 and sp[i] > max_odd:
        max_odd = sp[i]
        max_odd_index = i
        odd_exists = True

if not (even_exists or odd_exists):
    print('Отсутствует четный или нечетный элемент')
else:
    sp[max_odd_index] = min_even
    sp[min_even_index] = max_odd
    print(f'Измененный список:', *sp)
