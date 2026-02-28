import re

# Перевод из 4 в 10
def from_4_to_decimal(num_str: str) -> int:

    if '.' in num_str:
        integer_part, fractional_part = num_str.split('.')
    else:
        integer_part, fractional_part = num_str, ''

    # Проверка на отрицательное число
    if integer_part[0] == '-':
        is_neg = True
        integer_part = integer_part[1:]
    else:
        is_neg = False

    # Перевод
    result = 0

    # Преобразование целой части
    integer_part = integer_part[::-1]
    for i in range(len(integer_part)):
        result += int(integer_part[i]) * (4 ** i)

    # Преобразование дробной части
    for i in range(len(fractional_part)):
        result += int(fractional_part[i]) * (4 ** -(i + 1))

    if is_neg:
        result *= -1

    return result

# Перевод из 10 в 4
def from_decimal_to_4(num: int) -> str:

    is_neg = num < 0
    num = abs(num)

    integer_part = int(num)
    fractional_part = num - integer_part

    # Преобразование целой части
    integer_base4 = ''
    if integer_part == 0:
        integer_base4 = '0'
    while integer_part > 0:
        integer_base4 += str(integer_part % 4)
        integer_part //= 4
    integer_base4 = integer_base4[::-1]

    #Преобразование дробной части (Точность 5 знаков)

    if fractional_part == 0:
        result = integer_base4
    else:
        fractional_base4 = ''
        for _ in range(5):
            fractional_part *= 4
            digit = int(fractional_part)
            fractional_base4 += str(digit)
            fractional_part -= digit
            if fractional_part == 0:
                break

        result = integer_base4 + '.' + fractional_base4

    return '-' + result if is_neg else result


# Функция подсчета
def calculate(input_string):
    pattern = r'^(-?[0-3]+[.]?[0-3]*)([+-])([0-3]+[.]?[0-3]*)$'

    parse = re.match(pattern, input_string)

    if not parse:
        return "Неправильный ввод"

    num1 = parse.group(1)
    operator = parse.group(2)
    num2 = parse.group(3)

    num1 = from_4_to_decimal(num1)
    num2 = from_4_to_decimal(num2)

    if operator == '+':
        result = num1 + num2
    else:
        result = num1 - num2

    return from_decimal_to_4(result)

