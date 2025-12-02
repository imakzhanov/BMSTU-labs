'''
Макжанов Илья ИУ7-16Б
Лаораторная Работа 12
сложение и вычитание, Вариант 4
'''


def left_alignment(array):  # выравнивание по левому краю
    for i in range(len(array)):
        line = array[i].split()
        array[i] = ' '.join(line)

    return array


def right_alignment(array):  # выравнивание по правому краю
    max_line_len = len(max(array, key=len))  # длина самой длинной строки
    for i in range(len(array)):
        line = array[i].split()
        array[i] = ' '.join(line).rjust(max_line_len)

    return array


def width_alignment(array):  # выравнивание по ширине
    max_line_len = len(max(array, key=len))  # длина самой длинной строки
    for i in range(len(array)):
        line = array[i].split()
        line_len = sum(len(word) for word in line)  # длина строки без пробелов
        word_count = len(line)  # количество слов в строке

        space_amount = (max_line_len - line_len) // (word_count - 1)
        space_remain = (max_line_len - line_len) % (word_count - 1)
        line = (' ' * space_amount).join(line[:-1]) + ' ' * (space_amount + space_remain) + line[-1]
        array[i] = line

    return array


def del_word(array):  # удаление всех вхождений заданного слова
    input_word = input('\nВведите слово для удаления: ')
    for i in range(len(array)):
        array[i] = array[i].replace(input_word, '')

    return array


def word_replace(array):  # замена одного слова другим во всем тексте
    word_to_remove = input('\nВведите слово, которое нужно заменить: ')
    word_to_paste = input('\nВведите слово, на которое нужно заменить: ')
    for i in range(len(array)):
        array[i] = array[i].replace(word_to_remove, word_to_paste)

    return array


def expression_calculation(array):  # вычисление арифм. выражения
    digits = '0123456789'

    for i in range(len(array)):
        start, end = 0, 0
        value = 0  # значение арифм. выражения
        last_num = ''
        last_sign = ''

        while end < len(array[i]):
            if start == end:
                if array[i][end] in digits:  # начало арифм выраж.
                    last_num += array[i][end]
                    last_sign = '+'
                    end += 1
                else:
                    start, end = start + 1, end + 1
            elif start < end:
                if array[i][end] in digits:
                    last_num += array[i][end]
                    end += 1
                elif array[i][end] in '+-':
                    if last_num.strip() != '':
                        if last_sign == '+':
                            value += int(last_num)
                        else:
                            value -= int(last_num)

                    last_num = ''
                    last_sign = array[i][end]

                    end += 1
                else:  # конец выражения
                    if last_num.strip() != '':
                        if last_sign == '+':
                            value += int(last_num)
                        else:
                            value -= int(last_num)

                    array[i] = array[i][:start] + str(value) + ' ' + array[i][end:]

                    start += len(str(value))
                    end = start

                    value = 0
                    last_num = ''
                    last_sign = ''

        if start < end: # проверка для выражения в конце строки
            if last_num.strip() != '':
                if last_sign == '+':
                    value += int(last_num)
                else:
                    value -= int(last_num)

            array[i] = array[i][:start] + str(value) + ' ' + array[i][end:]

    return array


def del_shortest_word(array):  # удаление самого короткого слова в самом длинном предложении
    max_sentence_len = 0
    min_word_len = 0
    min_word_index = None  # индекс начала искомого слова

    curr_sentence_len = 0  # длина текущего предложения
    curr_min_word_len = float('+inf')  # длина мин. слова в текущем предложении
    curr_word_index = None  # индекс начала мин. слова в текущем предложении

    for i in range(len(array)):  # нахождение индекса начала и длины самого короткого слова
        curr_word = ''
        for j in range(len(array[i])):
            if array[i][j] == '.':  # конец предложения
                if curr_word != '':
                    curr_sentence_len += 1

                    if len(curr_word) < curr_min_word_len:  # проверка самого короткого слова
                        curr_min_word_len = len(curr_word)
                        curr_word_index = [i, j - len(curr_word)]

                if curr_sentence_len > max_sentence_len:  # проверка длины предложения
                    max_sentence_len = curr_sentence_len
                    min_word_len = curr_min_word_len
                    min_word_index = curr_word_index

                curr_sentence_len = 0
                curr_min_word_len = float('+inf')
                curr_word = ''

            elif array[i][j] in ' ,' and curr_word != '':  # конец слова
                curr_sentence_len += 1

                if len(curr_word) < curr_min_word_len:  # проверка самого короткого слова
                    curr_min_word_len = len(curr_word)
                    curr_word_index = [i, j - len(curr_word)]

                curr_word = ''

            elif array[i][j] not in ' ,':  # продолжение слова
                curr_word += array[i][j]

        if curr_word != '':  # конец строки, добавляем слово
            curr_sentence_len += 1
            if len(curr_word) < curr_min_word_len:  # проверка самого короткого слова
                curr_min_word_len = len(curr_word)
                curr_word_index = [i, j - len(curr_word)]


    # вывод и удаление слова
    if min_word_index != None:
        line = array[min_word_index[0]]
        print(f'\nНайденное слово: {line[min_word_index[1]:min_word_index[1] + min_word_len]}')
        line = line[:min_word_index[1]] + line[min_word_index[1] + min_word_len:]
        array[min_word_index[0]] = line
    else:
        print('Слово не найдено')

    return array


def del_empty_lines(array):  # удаление пустых строчек
    i = 0
    while i < len(array):
        if array[i] == '':
            array.pop(i)
        else:
            i += 1
    return array


def print_text(array):  # вывод текста
    print('\n' + '=' * len(max(array, key=len)))
    for i in array:
        print(i)
    print('=' * len(max(array, key=len)) + '\n')


def print_menu():  # вывод меню программы
    menu_list = ['1 - Выровнять текст по левому краю.',
                 '2 - Выровнять текст по правому краю.',
                 '3 - Выровнять текст по ширине.',
                 '4 - Удаление всех вхождений заданного слова.',
                 '5 - Замена одного слова другим во всём тексте.',
                 '6 - Вычисление арифметических выражений над целыми числами внутри текста',
                 '7 - Найти и удалить самое короткое слово в предложении, в котором слов больше всего',
                 'q - завершить программу'
                 ]
    for i in menu_list:
        print(i)


text = ['В,    плаще с кровавым подбоем, шаркающей кавалерийской походкой,',
        'рано утром 20-7+1 числа      весеннего месяца нисана ',
        'в крытую колоннаду между двумя крыльями    дворца Ирода Великого',
        '  вышел прокуратор     Иудеи Понтий Пилат. Более всего ',
        ' на свете прокуратор ненавидел запах розового масла,',
        'и всё  теперь       предвещало нехороший   2-1+2+21       день,',
        'потому что этот запах начал преследовать прокуратора с ',
        'рассвета. Он казался, что розовый запах источают кипарисы и пальмы в саду.']

while True:
    text = del_empty_lines(text)
    print_text(text)
    print_menu()

    input_num = input('\nВведите номер действия: ')
    match input_num:
        case '1':
            text = left_alignment(text)
        case '2':
            text = right_alignment(text)
        case '3':
            text = width_alignment(text)
        case '4':
            text = del_word(text)
        case '5':
            text = word_replace(text)
        case '6':
            text = expression_calculation(text)
        case '7':
            text = del_shortest_word(text)
        case 'q':
            print('\nПрограмма завершена.')
            break
        case _:
            print('\nПовторите ввод')

'''
найти и удалить предложение, содержащее зажанное слово наиб. количество раз
'''