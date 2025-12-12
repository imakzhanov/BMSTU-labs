import os


def encode_line(line, separator=','):  # перевод строки в csv формат
    return f'{separator}'.join(str(i) for i in line)


def decode_line(line, separator=','):  # перевод строки в список
    return line.strip().split(separator)  # удаляем символы перехода строки


def decode_types(line: str):  # перевод списка строк с типами в список типов
    all_types_dict = {
        "<class 'str'>": str,
        "<class 'int'>": int,
        "<class 'float'>": float
    }

    if not len(line):
        return line

    line = decode_line(line)
    for i in range(len(line)):
        el_type = all_types_dict.get(line[i])
        if el_type is None:
            raise ValueError(f'Неправильный тип файла!!!')
        else:
            line[i] = el_type
    return line


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
                elif extension == '.csv':  # выбираем этот файл и возвращаем его путь
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
            curr_path += '\\' + input_action + '.csv'
            break
        else:
            print('Невозможно создать файл без названия')

    return curr_path


def create_table(path: str):  # инициализация базы данных
    titles = input('Введите поля таблицы(через пробел): ').split()
    types = []
    for title in titles:
        while True:
            type = input('1. str\n'
                         '2. int\n'
                         '3. float\n'
                         f'Выберите тип данных для поля {title}: ')
            match type:
                case '1':
                    types.append(str)
                case '2':
                    types.append(int)
                case '3':
                    types.append(float)
                case _:
                    print('Неправильный ввод')
                    continue
            break

    with open(path, 'w', encoding='utf-8') as file:
        file.write(encode_line(titles) + '\n' + encode_line(types) + '\n')
    # заполняем таблицу
    fill_table(path, titles, types)


def fill_table(file_path: str, titles: list[str] = None, types: list[type] = None):  # заполнение таблицы
    if os.path.exists(file_path):  # проверка существования файла
        if titles is None and types is None:
            titles, types = read_title(file_path)

        print(f'Названия столбцов: ', end='')
        print_line(titles)
        print(f'Типы столбцов: ', end='')
        print_line(types)

        with open(file_path, 'a', encoding='utf-8') as file:
            while True:
                input_line = input(f'Введите строчку через пробел (введите пустую строчку для конца ввода): ').split()
                if not input_line:
                    break
                if check_input_line(input_line, types):  # проверка совпадения типов данных
                    file.write(encode_line(input_line) + '\n')

    else:
        print('\nДанный файл не существует')


def find_data(file_path: str) -> dict:  # поиск данных

    if os.path.exists(file_path):  # проверка существования файла
        titles, types = read_title(file_path)

        print('Номера столбцов:')
        for i in range(len(titles)):
            print(f'{i + 1}: {titles[i].strip():^18}{str(types[i]).strip():^18}')

        while True:
            columns = input('Введите номер столбца (или 2 столбцов через пробел) для поиска: ').split()

            if len(columns) != 1 and len(columns) != 2:
                print('Введено неверное количество столбцов')
                continue

            conditionals = dict()  # условия вывода

            for i in columns:
                if not i.isdigit():
                    print('Ведено не число')
                    break
                i = int(i) - 1

                if 0 <= int(i) < len(titles):
                    print(f'Столбец {i + 1}: {titles[i]}')

                    match str(types[i]):
                        case "<class 'int'>" | "<class 'float'>":
                            sign = input('Введите знак(>, <, =): ')
                            if sign not in ['>', '<', '=']:
                                print('Введен неправильный знак')
                                break
                            number = input('Введите число для сравнения: ')
                            if not number.isdigit():
                                print('Введено не число')
                                break

                            conditionals[i] = [sign, number]

                        case "<class 'str'>":
                            word = input('Введите слово для проверки вхождения: ')
                            conditionals[i] = word

                else:
                    print('Введено неправильное число')
                    break

            return conditionals

    else:
        print('\nФайл не существует')


def check_input_line(line: list[str], types: list[type]) -> bool:  # проверка введенной строчки на совпадение типов
    if len(line) != len(types):
        print('Длина строки не совпадает с количеством полей таблицы')
        return False

    return True


def read_title(file_path: str): # возвращает список полей и их типов
    with open(file_path, 'r', encoding='utf-8') as file:
        titles = decode_line(file.readline())
        types = decode_types(file.readline())
    return titles, types


def print_table(file_path: str, conditionals: dict = None):  # вывод базы данных с условиями
    if os.path.exists(file_path):  # проверка существования файла
        print(f'{"Вывод данных":^50}')
        with open(file_path, 'r', encoding='utf-8') as file:
            titles = decode_line(file.readline())
            types = decode_types(file.readline())

            print_line(titles, title=True)
            for line in file:
                line = decode_line(line)

                is_approach = True

                if conditionals is not None:  # если есть условия для вывода
                    for i in range(len(line)):
                        if i in conditionals.keys():
                            if types[i] == int:  # проверка для числа
                                sign = conditionals[i][0]
                                number = int(conditionals[i][1])
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

                            elif types[i] == str: # проверка для строки
                                word = conditionals[i]
                                if word not in line[i]:
                                    is_approach = False
                                    break

                if is_approach:
                    print_line(line)

    else:
        print('\nФайл не существует')


def print_line(list_a: list, field_len=18, title=False):  # вывод строки
    for i in list_a:
        print(f'{str(i).strip():^{field_len}}', end='')
    if title:
        print('\n' + '-' * len(list_a) * field_len)
    else:
        print()
