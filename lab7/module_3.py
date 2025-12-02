
# Вариант 4

print('\nМодуль 3: Поиск элемента с наибольшим числом идущих подряд пробелов\n')

array = []
el = input('Введите элемента списка (Enter - стоп): ')
while el:
    array.append(el)
    el = input('Введите элемента списка (Enter - стоп): ')

max_space_len = 0 # Длина максимальной цепочки пробелов
if not array: # проверка на пустой список
    print('Введен пустой список!')
    exit()
ans = array[0]

for i in array:
    current_space_len = 0
    for char in i: # Проходим по всем символам строки
        if char == ' ':
            current_space_len += 1
        else:
            if current_space_len > max_space_len: # проверка длины цепочки
                max_space_len = current_space_len
                ans = i
            current_space_len = 0

    if current_space_len > max_space_len: # проверка длины цепочки
        max_space_len = current_space_len
        ans = i

print('\nЭлемент с максимальным количеством идущих подряд пробелов:', ans)
