import struct
import os.path

'''
После каждого положительного числа добавить его удвоенное значение 
'''

file_name = 'file2.bin'

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


with open(file_name, 'rb+') as file:
    # 1 проход, считаем все положительные числа
    old_index = os.path.getsize(file_name) - 4
    new_index = old_index
    while True:
        try:
            num = struct.unpack('i', file.read(4))[0]
            if num > 0:
                new_index += 4
        except:
            break

    file.truncate(new_index)

    # 2 проход
    while new_index > old_index:
        file.seek(old_index)
        num = struct.unpack('i', file.read(4))[0]
        if num > 0:
            file.seek(new_index)
            file.write(struct.pack('i', num * 2))
            new_index -= 4
            file.seek(new_index)
            file.write(struct.pack('i', num))
        else:
            file.seek(new_index)
            file.write(struct.pack('i', num))

        old_index -= 4
        new_index -= 4

# Вывод
with open(file_name, 'rb+') as file:
    print('Измененный список: ')
    while True:
        try:
            num = struct.unpack('i', file.read(4))[0]
            print(num, end=' ')
        except:
            break
