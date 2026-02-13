
# Вариант 5

print('\nМодуль 2: Добавление после всех отрицательных элементов их удвоенного значения\n')

array = list(map(int, input('Введите список (числа через пробел): ').split()))
old_pos = len(array) - 1 # индекс последнего элемента исходного списка
new_pos = old_pos # индекс последнего элемента нового списка

for i in range(len(array)):
    if array[i] < 0:
        array = array + [None]
        new_pos += 1 # Увеличиваем индекс посл. элемента нового списка

while new_pos != old_pos:
    if array[old_pos] < 0:
        array[new_pos] = array[old_pos] * 2 # Записываем удвоенное значение
        new_pos -= 1
        array[new_pos] = array[old_pos] # Потом записываем его значение
    else:
        array[new_pos] = array[old_pos]

    new_pos, old_pos = new_pos - 1, old_pos - 1 # Умешьшаем указатели

print('\nИзмененный список:', *array)
