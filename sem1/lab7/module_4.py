
# вариант 1

print('\nМодуль 4: Замена всех строчных согласных английских букв на заглавные.\n')

alphabet = 'bcdfghjklmnpqrstvwxz' # все строчные согласные английские буквы

array = []
el = input('Введите элемента списка (Enter - стоп): ')
while el:
    array.append(el)
    el = input('Введите элемента списка (Enter - стоп): ')

for i in range(len(array)):
    char_index = 0
    while char_index < len(array[i]):
        if array[i][char_index] in alphabet:
            array[i] = array[i][:char_index] + array[i][char_index].upper() + array[i][char_index + 1:]
        char_index += 1

print('\nИзмененный список:', *array)
