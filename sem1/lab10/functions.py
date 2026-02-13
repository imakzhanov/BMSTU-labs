
from random import randint
import time

def quick_sort(list_a): # бытрая сортировка со счетчиком
    if len(list_a) <= 1:
        return list_a, 0

    pivot = list_a[len(list_a) // 2] # опорный элемент
    left = []
    middle = []
    right = []

    for element in list_a:
        if element < pivot:
            left.append(element)
        elif element == pivot:
            middle.append(element)
        else:
            right.append(element)

    permutations = len(left) + len(right)

    # рекурсивно сортируем левую и правую части
    left_part_sorted, left_permutations = quick_sort(left)
    right_part_sorted, right_permutations = quick_sort(right)

    return left_part_sorted + middle + right_part_sorted, left_permutations + right_permutations + permutations


def timer_quick_sort(list_a): # измерение времени для быстрой сортировки
    start_time = time.time()
    sorted_list_a, permutations = quick_sort(list_a)
    end_time = time.time()
    return sorted_list_a, permutations, (end_time - start_time) / 1000


def is_number(str): # проверка строки на положительное число, также может быть в экспоненциальной форме
    digits = '0123456789'
    is_exp = False
    num = ''
    num_exp = ''

    for i in range(len(str)):
        if is_exp:
            if str[i] not in digits:
                return False
            else:
                num_exp += str[i]
        elif str[i] == 'e' or str[i] == 'E':
            if len(num) == 0:
                return False
            is_exp = True
        elif str[i] in digits:
            num += str[i]
        else:
            return False
    if num_exp != '':
        return True
    return False


def ordered_lists_generator(sizes): # упорядоченные списки
    lists = []
    for i in sizes:
        lists.append(list(range(1, i + 1)))
    return lists

def random_lists_generator(sizes): # случайные списки
    lists = []
    for i in sizes:
        lists.append(list(randint(1, 10_000) for _ in range(i)))
    return lists

def reversed_lists_generator(sizes): # упорядоченные в обратном порядке списки
    lists = []
    for i in sizes:
        lists.append(list(range(i, 0, -1)))
    return lists

