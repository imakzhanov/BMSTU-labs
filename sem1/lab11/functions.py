
def is_num(string):  # Проверка на любое число
    digits = '0123456789'
    is_float = False
    is_exp = False
    num = ''
    num_after_exp = ''

    if string: # срезаем первый минус
        if string[0] == '-':
            string = string[1:]

    if string:
        for i in string:
            if is_exp:
                if num_after_exp == '':
                    if i in digits or i == '-':
                        num_after_exp = i
                    else:
                        return False
                else:
                    if i in digits:
                        num_after_exp += i
                    else:
                        return False
            elif i == 'e':
                if num == '' or num == '-':
                    return False
                is_exp = True

            else: # собираем первую часть числа, до экспоненты
                if is_float:
                    if i not in digits:
                        return False
                elif i == '.':
                    if num == '':
                        return False
                    is_float = True
                else:
                    if i not in digits:
                        return False
                    else:
                        num += i
        return True
    else:
        return False

def is_int(str):  # проверка строки на целое положительное число, также может быть в экспоненциальной форме
    digits = '0123456789'
    is_exp = False
    num = ''
    num_exp = ''

    for i in range(len(str)):
        if is_exp:
            if str[i] not in digits:
                return False
            else:
                num_exp += str[i]
        elif str[i] == 'e' or str[i] == 'E':
            if len(num) == 0:
                return False
            is_exp = True
        elif str[i] in digits:
            num += str[i]
        else:
            return False
    if is_exp and num_exp == '':
        return False
    return True


def median_rectangle_method(f, x_start, x_end, n):  # метод срединных прямоугольников
    s = 0
    x_step = (x_end - x_start) / n
    for i in range(n):
        x_value = x_start + i * x_step
        s += f(x_value + x_step / 2) * x_step
    return s


def three_eight_method(f, x_start, x_end, n):  # метод Симпсона 3/8
    if n % 3 != 0: # применение этого метода невозможно
        return False

    x_step = (x_end - x_start) / n
    s = f(x_start) + f(x_end)
    for i in range(1, n):
        x_value = x_start + i * x_step
        if i % 3 == 0:
            s += 2 * f(x_value)
        else:
            s += 3 * f(x_value)
    s *= 3 * x_step / 8
    return s
