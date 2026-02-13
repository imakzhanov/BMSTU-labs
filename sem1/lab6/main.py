
'''
Макжанов Илья Игоревич ИУ7-16Б
варианты 10, 5
'''

ex_num = input('Введите номер модуля (1a, 1b, 2a, 2b, 3, 4, 5): ')
match ex_num:
    case '1a':
        import module_1a
    case '1b':
        import module_1b
    case '2a':
        import module_2a
    case '2b':
        import module_2b
    case '3':
        import module_3
    case '4':
        import module_4
    case '5':
        import module_5
    case _:
        print('Невеный номер модуля!!!')