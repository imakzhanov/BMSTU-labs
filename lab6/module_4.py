
'''
Макжанов Илья Игоревич ИУ7-16Б
Задание 4, вариант 10
'''

print('\nМодуль 4, нахождение наиболее динной возраст. послед. отрицательных простых чисел')
sp = list(map(int, input('\nВведите список (числа через пробел): ').split()))

start, end = 0, 0
ans = []
while end < len(sp):
    if abs(sp[end]) == 1:  # Проверка на единицу (не простое число)
        is_prime = False
    else:
        for i in range(2, int(abs(sp[end])**0.5) + 1): # проверка 'текущего' числа на простоту
            if abs(sp[end]) % i == 0:
                is_prime = False
        else:
            is_prime = True

    if start == end and sp[end] < 0 and is_prime: # первое число послед.
        end += 1
    elif is_prime and sp[end] < 0 and sp[end] > sp[end - 1]:
        end += 1
    else: # конец последовательности
        if end - start + 1 > len(ans): # проверка длины текущей последовательности
            ans = sp[start:end] # элемент с индексом end не входит в последовательность
        if sp[end] < 0 and is_prime: # Подходит ли элемент под начало новой послед.
            start = end
        else: # если нет, то пропускаем элемент
            start, end = end + 1, end + 1

# Проверка длины последней послед.
if end - start + 1 > len(ans):
    ans = sp[start:end]

print(f'Наиболее длинная послед.:', *ans)
