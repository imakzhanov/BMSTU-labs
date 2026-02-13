'''
сложение и умножение со скобками
'''

def replace_inner_expression(string):
    digits = '0123456789'

    start, end = 0, 0
    expression = ''

    while end < len(string): # считаем все скобки
        if start == end:
            if string[end] == '(':
                expression += string[end]
            else:
                start += 1
            end += 1

        else:
            if string[end] in digits or string[end] in '+*':
                expression += string[end]
                end += 1
            elif string[end] == ')':
                expression += string[end]
                end += 1

                if expression[1:-1]: # проверяем на пустые скобки
                    value = calculate_expression(expression[1:-1])
                else:
                    value = expression

                string = string[:start] + str(value) + string[end:]

                expression = ''
                start += len(str(value))
                end = start

            else:
                end += 1
                start = end

    return string


def replace_expressions(string):
    digits = '0123456789'

    string = replace_inner_expression(string) # заменяем все выражения в скобках

    start, end = 0, 0
    expression = ''

    while end < len(string):
        if start == end:
            if string[end] in digits:
                expression += string[end]
            else:
                start += 1
            end += 1
        else:
            if string[end] in digits or string[end] in '+*':
                expression += string[end]
                end += 1
            else:
                value = calculate_expression(expression)
                string = string[:start] + str(value) + string[end:]

                expression = ''
                start += len(str(value))
                end = start

    if expression: # проверка для выражения на конце строки
        value = calculate_expression(expression)
        string = string[:start] + str(value) + string[end:]


    return string


def calculate_expression(expression): # считает арифм. выражния с + и *
    expression = expression.split('+')
    for i in range(len(expression)):
        if '*' in expression[i]:
            expression[i] = expression[i].split('*')
            mult_value = 1
            for j in expression[i]:
                mult_value *= int(j)
            expression[i] = str(mult_value)

    expr_value = sum(int(i) for i in expression)

    return expr_value

string = '2+3рано утром (2) 20+(20+7*2) 10 2*(1+2*3)+1*2 () числа 1+2'


string = replace_expressions(string)
print(string)
