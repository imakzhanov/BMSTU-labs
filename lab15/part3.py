import struct
import os.path

'''
быстрая сортировка 
'''


def quick_sort_binary_file(file_path, record_size):
    """
    Сортировка бинарного файла быстрой сортировкой in-place

    Args:
        file_path: путь к файлу
        record_size: размер одной записи в байтах
        key_func: функция для извлечения ключа из записи (опционально)
    """

    def read_num(pos):
        """Чтение записи по позиции (в записях, не байтах)"""
        with open(file_path, 'rb') as f:
            f.seek(pos * record_size)
            return f.read(record_size)

    def write_num(pos, data):
        """Запись записи по позиции"""
        with open(file_path, 'r+b') as f:
            f.seek(pos * record_size)
            f.write(data)

    def swap_nums(i, j):
        """Обмен двух записей местами"""
        if i == j:
            return
        data_i = read_num(i)
        data_j = read_num(j)
        write_num(j, data_i)
        write_num(i, data_j)

    def get_value(pos):
        """Получение ключа записи"""
        data = read_num(pos)
        return struct.unpack('i', data[:4])[0]

    def partition(left, right):
        """Разделение для быстрой сортировки"""
        pivot_pos = (left + right) // 2
        pivot_value = get_value(pivot_pos)
        print(pivot_value)
        # Перемещаем опорный элемент в конец
        swap_nums(pivot_pos, right)

        store_index = left
        for i in range(left, right):
            if get_value(i) <= pivot_value:
                swap_nums(i, store_index)
                store_index += 1

        # Возвращаем опорный элемент на правильное место
        swap_nums(store_index, right)
        return store_index

    def quick_sort_range(left, right):
        """Итеративная быстрая сортировка для диапазона записей"""
        stack = [(left, right)]

        while stack:
            l, r = stack.pop()

            if l >= r:
                continue

            pivot_index = partition(l, r)

            # Сначала добавляем больший подмассив, чтобы уменьшить глубину стека
            left_size = pivot_index - 1 - l
            right_size = r - (pivot_index + 1)

            if left_size > right_size:
                stack.append((l, pivot_index - 1))
                stack.append((pivot_index + 1, r))
            else:
                stack.append((pivot_index + 1, r))
                stack.append((l, pivot_index - 1))

    # Определяем количество записей в файле
    file_size = os.path.getsize(file_path)
    num_records = file_size // record_size

    # Запускаем сортировку
    quick_sort_range(0, num_records - 1)


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


quick_sort_binary_file(file_name, 4)


# Вывод
with open(file_name, 'rb+') as file:
    print('Измененный список: ')
    while True:
        try:
            num = struct.unpack('i', file.read(4))[0]
            print(num, end=' ')
        except:
            break
