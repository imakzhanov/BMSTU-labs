import struct
import os.path

'''
Удалить все Нечётные элементы
'''

file_name = 'file1.bin'

# Запись в файл
with open(file_name, 'wb') as file:
    while True:
        try:
            numbers = list(map(int, input('Введите список чисел через пробел: ').split()))
        except:
            print('Неправильный ввод')
            continue
        break

    for num in numbers:
        file.write(struct.pack('i', num))

# Удаление
with open(file_name, 'rb+') as file:
    odd_count = 0
    while True:
        try:
            num = struct.unpack('i', file.read(4))[0]
        except:
            break

        if num % 2 != 0:
            odd_count += 1
        else:
            poz = file.tell()
            file.seek(poz - (odd_count + 1) * 4)
            file.write(struct.pack('i', num))
            file.seek(poz)

    file.truncate(os.path.getsize(file_name) - odd_count * 4)

# Вывод
with open(file_name, 'rb+') as file:
    print('Измененный список: ')
    while True:
        try:
            num = struct.unpack('i', file.read(4))[0]
            print(num, end = ' ')
        except:
            break
