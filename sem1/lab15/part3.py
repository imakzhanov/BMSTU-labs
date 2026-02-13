import struct
import os.path

'''
простыми вставками
'''


file_name = 'file3.bin'

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
    file_size = os.path.getsize(file_name)
    for i in range(4, file_size, 4):
        file.seek(i)
        key = struct.unpack('i', file.read(4))[0]
        j = i - 4

        file.seek(j)
        num = struct.unpack('i', file.read(4))[0]
        while j >= 0 and key < num:
            file.seek(j)
            num = struct.unpack('i', file.read(4))[0]
            file.seek(j + 4)
            file.write(struct.pack('i', num))
            j -= 4

        file.seek(j + 4)
        file.write(struct.pack('i', key))


# Вывод
with open(file_name, 'rb+') as file:
    print('Измененный список: ')
    while True:
        try:
            num = struct.unpack('i', file.read(4))[0]
            print(num, end=' ')
        except:
            break
