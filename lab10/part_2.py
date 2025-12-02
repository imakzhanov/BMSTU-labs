from random import randint
from functions import *

# Ввод данных
n1 = input('Введите размерность N1: ')
if not is_number(n1):
    exit('Введено не число')
n1 = int(n1)

n2 = input('Введите рамерность N2: ')
if not is_number(n2):
    exit('Введено не число')
n2 = int(n2)

if n2 - n1 < 9:
    exit('разница между N1 и N2 должна превышать 9')


# Подсчет времени сортировки
ordered_lists_times = [] # время сортировки для упорядоченных списков
random_lists_times = [] # время сортировки для случайных списков
reversed_lists_times = [] # время сортировки для обратно упорядоченных списков

len_step = int((n2 - n1) / 9) # шаг для длины массивов
len_value = n1

while len_value <= n2:
    ordered_list = list(range(1, len_value + 1)) # упорядоченный список
    random_list = list(randint(1, 10_000) for _ in range(len_value)) # случайный список
    reversed_list = list(range(len_value, 0, -1)) # обратный список

    ordered_lists_times.append(timer_quick_sort(ordered_list)[2])
    random_lists_times.append(timer_quick_sort(random_list)[2])
    reversed_lists_times.append(timer_quick_sort(reversed_list)[2])

    len_value += len_step

# на оси t 5 засечек
min_time = min(min(ordered_lists_times), min(random_lists_times), min(reversed_lists_times))
max_time = max(max(ordered_lists_times), max(random_lists_times), max(reversed_lists_times))


# Построение оси t
time_step =(max_time - min_time) / 4
last_serif_len = 0
print(f'{'':^10}|', end = '')
for i in range(5):
    time_value = round(min_time + i * time_step, 8)  # значение функции для оси OY
    serif_position = int((time_value - min_time) * 100 // (max_time - min_time))
    print(' ' * (serif_position - last_serif_len) + f'{time_value}', end ='')
    last_serif_len = len(str(time_value)) + serif_position
print()

# Построение графика
# + - для упорядоченного списка
# * - для сгенерированного списка
# - - для обратно упорядоченного списка


len_value = n1
for i in range(len(ordered_lists_times)):
    print(f'{len_value:^10}|', end = '')
    line = [' '] * 101

    # Позиции точек для списков
    ordered_poz = int((ordered_lists_times[i] - min_time) * 100 // (max_time - min_time))
    random_poz = int((random_lists_times[i] - min_time) * 100 // (max_time - min_time))
    reversed_poz = int((reversed_lists_times[i] - min_time) * 100 // (max_time - min_time))

    line[ordered_poz] = '+'
    line[random_poz] = '*'
    line[reversed_poz] = '-'

    print(''.join(line))

    len_value += len_step

'''
вставка с барьерами
'''
