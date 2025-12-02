

list_a = list(map(int, input('\nВведите список (числа через пробел): ').split()))

min_el = list_a[0]
second_min = list_a[1]
if second_min < min_el:
    min_el, second_min = second_min, min_el

for i in list_a:
    if i < min_el:
        second_min = min_el
        min_el = i
    elif i > min_el and i < second_min:
        second_min = i

print(f'\nВторое по величине значение: {second_min}')