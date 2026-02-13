
# Вариант 1

print('\nМодуль 1: Удаление всех нулевых элементов списка\n')

array = list(map(int, input('Введите список (числа через пробел): ').split()))
list_len = len(array)  # длина исходного списка
zero_count = 0  # Счетчик нулей

for i in range(list_len):
    if array[i] == 0:
        zero_count += 1  # Увеличиваем счетчик
    else:
        array[i - zero_count] = array[i]  # смещаем все ненулевые элементы  начало

array = array[:list_len - zero_count]  # удаляем все нули в конце списка

print('\nСписок с удаленными нулями:', *array)