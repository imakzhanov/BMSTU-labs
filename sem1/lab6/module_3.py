
'''
Макжанов Илья Игоревич ИУ7-16Б
'''

print('\nМодуль 3, нахождение K-того экстемума в списке')

sp = list(map(int, input('\nВведите список (числа через пробел): ').split()))
k = int(input('Введите число K: '))

for i in range(len(sp) - 2):
    if ((sp[i + 1] < sp[i] and sp[i + 1] < sp[i + 2])
        or (sp[i + 1] > sp[i] and sp[i + 1] > sp[i + 2])): # экстремум
        k -= 1

    if k == 0:
        print(f'K-тый экстремум: {sp[i + 1]}')
        break
else:
    print('К-того экстремума не существует')