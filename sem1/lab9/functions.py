
def is_number(s):
    if s:
        if s[0] == '-':
            s = s[1:]
    else:
        return False
    if s:
        for i in s:
            if i < '0' or i > '9':
                return False
        return True
    return False

def matrix_print(matrix, matrix_rows, matrix_columns): # вывод матрицы
    for i in range(matrix_rows):
        for j in range(matrix_columns):
            print(f'{matrix[i][j]:^6.3g}', end='')
        print()