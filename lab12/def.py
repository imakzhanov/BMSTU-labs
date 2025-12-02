'''
найти и удалить предложение, содержащее зажанное слово наиб. количество раз
'''

def print_text(array):  # вывод текста
    print('\n' + '=' * len(max(array, key=len)))
    for i in array:
        print(i)
    print('=' * len(max(array, key=len)) + '\n')



def find_sentences(array):
    sentences = []

    curr_sentence = ''
    start_pos = [0, 0]
    end_pos = [0, 0]
    for i in range(len(array)):
        for j in range(len(array[i])):
            if array == '.':
                end_pos = [i, j + 1]
                sentences.append(curr_sentence, start_pos, end_pos)
            else:
                if curr_sentence ==  '':
                    start_pos = [i, j]
                curr_sentence = array[i][j]

    return sentences

def del_sentence(array, word):
    sentences = find_sentences(array)
    for i in sentences:
        print(i)

    sentence_del_index = -1
    max_count = 0
    for i in range(len(sentences)):
        if sentences[i][0].count(word) > max_count:
            max_count = sentences[i][0].count(word)
            sentence_del_index = i

    start = sentences[sentence_del_index][1]
    end = sentences[sentence_del_index][2]

    array[start[0]] = array[:start[1]]
    array[end[0]] = array[end[1]:]


text = ['В,    плаще с кровавым подбоем, шаркающей кавалерийской походкой,',
        'рано утром 20-7+1 числа      весеннего месяца нисана ',
        'в крытую колоннаду между двумя крыльями    дворца Ирода Великого',
        '  вышел прокуратор     Иудеи Понтий Пилат. Более всего ',
        ' на свете прокуратор ненавидел запах розового масла,',
        'и всё  теперь       предвещало нехороший   2-1+2+21       день,',
        'потому что этот запах начал преследовать прокуратора с ',
        'рассвета. Он казался, что розовый запах источают кипарисы и пальмы в саду.']

while True:
    print_text(text)
    input_word = input('\nВведите слово: ')
    text = del_sentence(text, input_word)