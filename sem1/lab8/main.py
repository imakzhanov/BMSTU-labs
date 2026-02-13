
'''
Макжанов Илья Игоревич ИУ7-16Б
Лабораторная №8
варианты 3, 2
'''

module_number = input('Введите номер модуля: ')
match module_number:
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
    case _:
        exit('Неверный номер модуля!!!')