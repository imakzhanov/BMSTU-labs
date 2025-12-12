import os


def encode_line(line, separator=','):  # перевод строки в csv формат
    return f'{separator}'.join(str(i) for i in line)


def decode_line(line, separator=','):  # перевод строки в список
    return line.split(separator)


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
        line[i] = line[i].strip()   # удаляем символы перехода строки
        el_type = all_types_dict.get(line[i])
        if el_type is None:
            raise ValueError(f'Неправильный тип файла!!!')
        else:
            line[i] = el_type
    return line


def choose_dir():  # выбор пути для создания бд

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
                             '2) Введите . чтобы перейти в родительский католог\n'
                             '3) Введите название файла для создания в текущей директории\n'
                             'Выберите действие: ')

        if input_action.isdigit():  # переход в подкаталог
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
            if len(curr_path) == 1:  # проверка на корневой каталог
                print('\nВы находитесь в корневом каталоге')
            else:
                curr_path = curr_path[:-1]
            curr_path = '\\'.join(curr_path)

        elif input_action != '':  # создаем csv файл в текущем каталоге
            curr_path += '\\' + input_action + '.csv'
            break
        else:
            print('Невозможно создать файл без названия')

    return curr_path


def create_table(path):  # инициализация базы данных
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


def fill_table(path, titles=None, types=None):  # заполнение таблицы
    if titles is None and types is None:
        titles, types = read_title(path)

    print(f'Названия столбцов: ', end='')
    print_line(titles)
    print(f'Типы столбцов: ', end='')
    print_line(types)

    with open(path, 'a', encoding='utf-8') as file:
        while True:
            input_line = input(f'Введите строчку через пробел (введите пустую строчку для конца ввода): ').split()
            if not input_line:
                break
            if check_input_line(input_line, types):  # проверка совпадения типов данных
                file.write(encode_line(input_line) + '\n')



def find_data(path):  # поиск данных
    titles, types = read_title(path)

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
                continue
            i = int(i) - 1

            if 0 <= int(i) < len(titles):
                print(f'Столбец {i + 1}: ')

                match str(types[i]):
                    case "<class 'int'>" | "<class 'float'>":
                        sign = input('Введите знак(>, <, =): ')
                        if sign not in ['>', '<', '=']:
                            print('Введен неправильный знак')
                            continue
                        number = input('Введите число для сравнения: ')
                        if not number.isdigit():
                            print('Введено не число')
                            continue

                        conditionals[i] = [sign, number]  # выводим

                    case "<class 'str'>":
                        word = input('Введите слово для проверки входжения: ')
                        conditionals[i] = word

            else:
                print('Введено неправильное число')
                continue

        return conditionals


def check_input_line(line: list[str], types: list[type]):  # проверка введенной строчки на совпадение типов
    if len(line) != len(types):
        print('Длина строки не совпадает с количеством полей таблицы')
        return False

    for i in range(len(line)):
        if ',' in line[i]:
            print('поле не может содержать , т. к. она является разделителем')
            return False

        try:
            element = types[i](line[i])
        except:
            print(f'{line[i]} не соответствует типу данных {types[i]}')
            return False
    return True


def read_title(path):
    with open(path, 'r', encoding='utf-8') as file:
        titles = decode_line(file.readline())
        types = decode_types(file.readline())
    return titles, types


def read_table(path, conditionals=None): # вывод базы данных с условиями
    print(f'{'Вывод данных':^50}')
    with open(path, 'r', encoding='utf-8') as file:
        titles = decode_line(file.readline())
        types = decode_types(file.readline())

        print_line(titles, title=True)
        for line in file:
            line = decode_line(line)

            is_approach = True

            if conditionals is not None:  # если есть условия для вывода
                for i in range(len(line)):
                    if i in conditionals.keys():
                        if type(conditionals[i]) == list:  # проверка для числа
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
                        elif type(conditionals[i]) == str:
                            word = conditionals[i]
                            if word not in line[i]:
                                is_approach = False
                                break

            if is_approach:
                print_line(line)


def print_line(list_a, field_len=18, title=False):  # вывод строки
    for i in list_a:
        print(f'{str(i).strip():^{field_len}}', end='')
    if title:
        print('\n' + '-' * len(list_a) * field_len)
    else:
        print()
