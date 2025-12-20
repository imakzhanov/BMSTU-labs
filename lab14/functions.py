import os
import struct


def print_line(line: list[str]):
    output_line = '|'
    for i in line:
        if type(i) == bytes:
            i = i.strip(b'\x00').decode()
        output_line += f'{i:^18}|'
    print(output_line)
    print('-' * (len(line) * 19 + 1))


def choose_dir() -> str:  # выбор пути для создания бд

    curr_path = os.getcwd()  # берем папку проекта за начальный путь
    while True:
        # Вывод текущей директории и всех файлов и папок в ней
        print('\n' + '=' * 100)
        print(f'Текущая директория: {curr_path}')
        print('=' * 100)
        all_items = os.listdir(curr_path)  # Список всех папок и файлов в текущей директории
        for i in range(len(all_items)):
            print(f'{i}: {all_items[i]}')
        print('=' * 100)

        # Выбор действия
        input_action = input('1) Введите номер каталога или файла чтобы перейти в него\n'
                             '2) Введите . чтобы перейти в родительский каталог\n'
                             '3) Введите название файла для создания в текущей директории\n'
                             'Выберите действие: ')

        if input_action.isdigit():  # переход в подкаталог, или открытие csv файла
            if 0 <= int(input_action) < len(all_items):
                try_path = curr_path + '\\' + all_items[int(input_action)]
                _, extension = os.path.splitext(try_path)

                if extension == '':  # переходим в папку
                    curr_path = try_path
                elif extension == '.bin':  # выбираем этот файл и возвращаем его путь
                    curr_path = try_path
                    break
                else:
                    print('\nДанный файл невозможно открыть')
            else:
                print('Введено неправильное число')

        elif input_action == '.':  # переходим в родительский каталог
            curr_path = curr_path.split('\\')
            if len(curr_path) <= 2:  # проверка на корневой каталог
                print('\nВы не можете перейти в родительский каталог')
            else:
                curr_path = curr_path[:-1]
            curr_path = '\\'.join(curr_path)

        elif input_action != '':  # создаем csv файл в текущем каталоге
            curr_path += '\\' + input_action + '.bin'
            break
        else:
            print('Невозможно создать файл без названия')

    return curr_path


def create_table(path: str):  # инициализация базы данных
    titles = input('Введите поля таблицы(через пробел): ').split()
    lines_format = ''
    title_format = ''.join(f'{len(i.encode())}s' for i in titles)
    for title in titles:
        while True:
            type = input('1. int\n'
                         '2. float\n'
                         '3. str\n'
                         f'Выберите тип данных для поля {title}: ')
            match type:
                case '1':
                    max_number = input('Введите максимально возможное число: ')
                    if not max_number.isdigit():
                        print('Введено не число')
                        continue
                    max_number = abs(int(max_number))

                    if max_number <= 2 ** 8 - 1:
                        lines_format += 'B'
                    elif max_number <= 2 ** 16 - 1:
                        lines_format += 'H'
                    elif max_number <= 2 ** 32 - 1:
                        lines_format += 'I'
                    else:
                        lines_format += 'Q'

                case '2':
                    accuracy = input('Введите нужную точность от 1 до 16: ')
                    if not accuracy.isdigit():
                        print('Введено не число')
                        continue
                    accuracy = int(accuracy)

                    if 1 <= accuracy <= 4:
                        lines_format += 'e'
                    elif 5 <= accuracy <= 8:
                        lines_format += 'f'
                    else:
                        lines_format += 'd'

                case '3':
                    max_len = input('Введите максимальную длину строки (в байтах): ')
                    if not max_len.isdigit():
                        print('Введено не число')
                        continue
                    max_len = int(max_len)

                    lines_format += f'{max_len}s'

                case _:
                    print('Неверный формат данных')
            break

    with open(path, 'wb') as file:
        file.write((lines_format + ';' + title_format + '\n').encode())  # записываем типы для данных и для заголовков
        file.write(struct.pack(title_format, *[i.encode() for i in titles]))


def find_data(path) -> dict | None:  # поиск по таблице
    if not does_file_exist(path):
        print('Файл не существует')
        return None

    with open(path, 'rb') as file:
        lines_format, title = read_title(path, file)
        clear_fmt = clean_format(lines_format)

        while True:
            print_line(title)
            try:
                columns = list(map(int, input(
                    'Введите по каким столбцам искать информацию (через пробел, начиная с нуля): ').split()))
            except:
                print('Неверный ввод')
                continue
            if len(columns) != 1 and len(columns) != 2:
                print('Неверное количество столбцов')
                continue
            elif min(columns) < 0 or max(columns) >= len(title):
                print('Неверный ввод')
                continue

            conditional = dict()

            for i in columns:
                print(f'Условие для поля {title[i]}: ')
                match clear_fmt[i]:
                    case 'B' | 'H' | 'I' | 'Q' | 'e' | 'f' | 'g':  # для int или float
                        sign = input('Введите знак для сравнения: ')
                        if sign not in ['<', '>', '=']:
                            print('Неверный ввод')
                            break
                        number = input('Введите число для сравнения: ')
                        if not number.isdigit():
                            print('Введено не число')
                            break

                        conditional[i] = [sign, number]

                    case 's':  # для str
                        word = input('Введите слово для проверки вхождения')
                        conditional[i] = word
                    case _:
                        raise ValueError('Неверный тип данных!')

            return conditional


def read_table(path: str, with_cond=False):  # вывод таблицы
    if not does_file_exist(path):
        print('Файл не существует')
        return None

    with open(path, 'rb') as file:
        lines_format, title = read_title(path, file)
        line_size = struct.calcsize(lines_format)
        clean_fmt = clean_format(lines_format)
        if with_cond:
            cond = find_data(path)

        print_line(title)
        while True:
            try:
                line = [i for i in struct.unpack(lines_format, file.read(line_size))]
                print(line)
            except:
                break
            if with_cond: # проверка строчки на условие
                is_approach = True
                for i in range(len(line)):
                    if i in cond.keys():
                        if clean_fmt[i] in ['B', 'H', 'I', 'Q', 'e', 'f', 'g']: # для int и float
                            sign, number = cond[i][0], int(cond[i][1])
                            match sign:
                                case '<':
                                    if not (float(line[i]) < number):
                                        is_approach = False
                                        break
                                case '>':
                                    if not (float(line[i]) > number):
                                        is_approach = False
                                        break
                                case '=':
                                    if float(line[i]) != number:
                                        is_approach = False
                                        break

                        elif clean_fmt[i] == 's':
                            if type(line[i]) == bytes:
                                line[i] = line[i].strip(b'\x00').decode()
                            word = cond[i]
                            if word not in line[i]:
                                is_approach = False
                                break

                if is_approach:
                    print_line(line)

            else:
                print_line(line)


def check_line(line: list[str], line_format: str) -> True | False:  # проверка соответствия типу
    clean_fmt = clean_format(line_format)
    try:
        for i in range(len(clean_fmt)):
            match clean_fmt[i]:
                case 'B' | 'H' | 'I' | 'Q':  # для int
                    line[i] = int(line[i])
                case 'e' | 'f' | 'g':  # для float
                    line[i] = float(line[i])
                case 's':  # для str
                    continue
                case _:
                    raise ValueError('Неверный тип данных!')
    except:
        print('Введенная строка не совпадает с типом')
        return False
    return True


def clean_format(format: str) -> str:  # преобразует формат в формат без длины(для проверки соответствия типу)
    clean_fmt = format
    for i in '0123456789':
        clean_fmt = clean_fmt.replace(i, '')
    return clean_fmt


def fill_table(path: str):
    if not does_file_exist(path):
        print('Файл не существует')
        return None

    lines_format, title = read_title(path)

    with open(path, 'ab') as file:
        while True:
            print_line(title)
            input_line = input('Введите одну строчку через пробел, введите пустую строчку для конца ввода: ')
            if not input_line:
                break
            input_line = input_line.split()
            if check_line(input_line, lines_format):
                try:
                    file.write(struct.pack(lines_format, *[i.encode() if type(i) == str else i for i in input_line]))
                except:
                    print('Введенная строка не удовлетворяет типам!')
            else:
                print('Введенная строка не удовлетворяет типам!')


def fill_by_index(path: str):  # запись в любое место
    if not does_file_exist(path):
        print('Файл не существует')
        return None

    with open(path, 'r+b') as file:
        while True:
            index = input('Введите на какую позицию вставить строчку (начиная с нулевой): ')
            if not index.isdigit() or int(index) < 0:
                print('Неправильный ввод')
                continue
            index = int(index)

            lines_format, title = read_title(path, file)
            line_size = struct.calcsize(lines_format)

            poz = file.tell() + line_size * index
            if os.path.getsize(path) < poz:
                print('Неправильный ввод')
                continue

            print_line(title)
            input_line = input('Введите строчку через пробел: ').split()
            if check_line(input_line, lines_format):
                for i in range(os.path.getsize(path), poz, -line_size):
                    file.seek(i - line_size)
                    line = file.read(line_size)
                    file.write(line)

                file.seek(poz)
                try:
                    file.write(struct.pack(lines_format, *[i.encode() if type(i) == str else i for i in input_line]))
                except:
                    print('Введенная строка не удовлетворяет типам!')
                break
            else:
                print('Введенная строка не удовлетворяет типам!')


def del_by_index(path: str):  # удаление по индексу
    if not does_file_exist(path):
        print('Файл не существует')
        return None

    with open(path, 'r+b') as file:
        while True:
            index = input('Введите номер строки для удаления (начиная с нулевой): ')
            if not index.isdigit() or int(index) < 0:
                print('Неправильный ввод')
                continue
            index = int(index)

            lines_format, title = read_title(path, file)
            line_size = struct.calcsize(lines_format)

            poz = file.tell() + line_size * index
            if os.path.getsize(path) < poz:
                print('Неправильный ввод')
                continue

            for i in range(poz, os.path.getsize(path) - line_size, line_size):
                file.seek(i + line_size)
                line = file.read(line_size)
                file.seek(i)
                file.write(line)

            file.truncate(os.path.getsize(path) - line_size)
            break


def read_title(path: str, file=None) -> tuple[str, list[str]]:  # считывание заголовка таблицы и типов
    if file is None:  # файл не открыт
        with open(path, 'rb') as file:
            lines_format, title_format = file.readline().decode().split(';')
            title_names = [i.decode() for i in struct.unpack(title_format, file.read(struct.calcsize(title_format)))]

    else:
        lines_format, title_format = file.readline().decode().split(';')
        title_names = [i.decode() for i in struct.unpack(title_format, file.read(struct.calcsize(title_format)))]

    return lines_format, title_names


def does_file_exist(path):
    return os.path.exists(path)
