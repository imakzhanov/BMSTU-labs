import os

from functions import decode_line, decode_types, encode_line


def sort_table(file_name: str):
    if os.path.exists(file_name):  # Проверка существования файла
        with open(file_name, 'r', encoding='utf-8') as file:

            titles = decode_line(file.readline())
            types = decode_types(file.readline())
            print('Номера столбцов:')
            for i in range(len(titles)):
                print(f'{i}: {titles[i].strip():^18}{str(types[i]).strip():^18}')

            # Ввод значений
            while True:
                try:
                    columns = list(
                        map(int, input('Введите номера столбцов для сортировки(в порядке приоритета): ').split()))
                except:
                    print('Введены не числа')
                    continue
                if min(columns) < 0 or max(columns) >= len(titles):
                    print('Не все значения верны')
                    continue
                break

            key_values = []  # список со значениями записей в нужных столбцах

            while True:
                pos = file.tell()
                line = file.readline()
                if not line:
                    break

                line = decode_line(line)
                key_values.append(list())
                for column in columns:
                    key_values[-1].append(types[column](line[column]))
                key_values[-1].append(pos)

            key_values.sort()

            file_path, extension = os.path.splitext(file_name)
            copy_file_name = file_path + '_copy' + extension  # создаем копию файла, куда перемещаем все данные в отсортированном виде

            with open(copy_file_name, 'w', encoding='utf-8') as file2:
                # записываем названия столбцов и их типы
                file2.write(encode_line(titles) + '\n' + encode_line(types) + '\n')

                for *_, index in key_values:
                    file.seek(index)
                    file2.write(file.readline())

        os.remove(file_name) # меняем начальный файл на файл-копию
        os.replace(copy_file_name, file_name)


    else:
        print('\nФайл не существует')
