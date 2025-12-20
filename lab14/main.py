from functions import *


def print_menu(path: str):
    menu_list = ['1. Выбрать файл для работы',
                 '2. Инициализировать базу данных',
                 '3. Вывести содержимое базы данных',
                 '4. Добавить запись в произвольное место базы данных',
                 '5. Добавить запись в конец базы данных',
                 '6. Удалить произвольную запись из базы данных',
                 '7. Поиск',
                 'q. Завершить программу'
                 ]

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
        case '1':
            curr_path = choose_dir()
        case '2':
            lines_format, titles = create_table(curr_path)
        case '3':
            read_table(curr_path)
        case '4':
            fill_by_index(curr_path)
        case '5':
            fill_table(curr_path)
        case '6':
            del_by_index(curr_path)
        case '7':
            read_table(curr_path, True)
        case 'q':
            print('Программа завершена')
            break
        case _:
            print('Введен неверный номер')

