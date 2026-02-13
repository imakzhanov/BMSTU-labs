
'''
Лабораторная работа 10
Макжанов Илья Игоревич ИУ7-16Б
Быстрая Сортировка
'''

from functions import *

# ввод списка
list_a = input('\nВведите список(числа через пробел): ').split()
if len(list_a) == 0:
    exit('Введен пустой список')
for i in range(len(list_a)):
    if not(is_number(list_a[i])):
        exit(f'{list_a[i]} не число')
    list_a[i] = int(float(list_a[i]))

# сортировка
sorted_list_a, list_a_permutations, list_a_time = timer_quick_sort(list_a)

# вывод
print('\nОтсортированный список:', sorted_list_a)
print(f'\nЗатраченное время(сек): {list_a_time} | Количество перестановок: {list_a_permutations}')


# ввод размерностей массивов
sizes = input('\nВведите 3 числа через пробел: ').split()
if len(sizes) != 3:
    exit('Неверное количество чисел')
for i in range(len(sizes)):
    if not(is_number(sizes[i])):
        exit(f'{sizes[i]} не число, или его запись некорректна')
    sizes[i] = int(float(sizes[i]))

# вывод таблицы
print('-' * 101)
print(f'|{' ':^24}|{sizes[0]:^24}|{sizes[1]:^24}|{sizes[2]:^24}|')
print('-' * 101)
print(f'|{' ':^24}|{'время(c)':^10}|{'перестановки':^13}'
      f'|{'время(c)':^10}|{'перестановки':^13}|{'время(c)':^10}|{'перестановки':^13}|')
print('-' * 101)

# Упорядоченные списки
print(f'|{'Упорядоченный список':^24}|', end = '')

ordered_lists = ordered_lists_generator(sizes) # создаем списки
for i in ordered_lists:
    sorted_list, permutations, sort_time = timer_quick_sort(i)
    print(f'{sort_time:^10.6f}|{permutations:^13}|', end = '')

print('\n' + '-'*101)

# Случайные списки
print(f'|{'Случайный список':^24}|', end = '')

random_lists = random_lists_generator(sizes) # создаем списки
for i in random_lists:
    sorted_list, permutations, sort_time = timer_quick_sort(i)
    print(f'{sort_time:^10.6f}|{permutations:^13}|', end = '')

print('\n' + '-'*101)

# Упорядоченные в обратном порядке списки
print(f'|{'Обратный список':^24}|', end = '')

reversed_lists = reversed_lists_generator(sizes) # создаем списки
for i in reversed_lists:
    sorted_list, permutations, sort_time = timer_quick_sort(i)
    print(f'{sort_time:^10.6f}|{permutations:^13}|', end = '')

print('\n' + '-'*101)