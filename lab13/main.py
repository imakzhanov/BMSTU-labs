
from functions import *


def print_menu(path = None):
    menu_list = ['1. Выбрать файл для работы',
                 '2. Инициализировать базу данных (создать'
                 ' либо перезаписать файл и заполнить его записями).',
                 '3. Вывести содержимое базы данных.',
                 '4. Добавить запись в конец базы данных.',
                 '5. Поиск в таблице.',
                 'q. Завершить программу.']

    print('\n' + '=' * 100)
    print(f'Текущая директория: {path}')
    print('=' * 100)
    for i in menu_list:
        print(i)
    print('=' * 100 + '\n')


curr_path = choose_dir()

while True:
    print_menu(curr_path)
    input_num = input('Введите номер: ')

    match input_num:
        case '1': # выбор файла
            curr_path = choose_dir()
        case '2': # инициализация бд
            create_table(curr_path)
        case '3':
            read_table(curr_path)
        case '4':
            fill_table(curr_path)
        case '5':
            conditions = find_data(curr_path)
            read_table(curr_path, conditions)
        case 'q':
            print('Программа завершена')
            break

        case _:
            print('Неверное число')

