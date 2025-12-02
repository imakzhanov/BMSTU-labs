"""
Макжанов Илья Игоревич
ИУ7-16Б
"""

module_num = input('\nВведите номер модуля(число от 1 до 7): ')
match module_num:
    case '1':
        import module_1
    case '2':
        import module_2
    case '3':
        import module_3
    case '4':
        import module_4
    case '5':
        import module_5
    case '6':
        import module_6
    case '7':
        import module_7
    case _:
        print('Введен неверный номер')