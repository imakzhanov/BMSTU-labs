import re

def validate(value): # валидация вводимой строки(не дает ввести посторонние символы)
    s = '0123+-,'
    for i in value:
        if i not in s:
            return False
    return True

