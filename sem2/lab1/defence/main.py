import tkinter as tk
from tkinter import ttk

def convert_4_to_10():
    num = entry_base4.get()

    if '.' in num:
        integer_part, fractional_part = num.split('.')
    else:
        integer_part, fractional_part = num, ''

    if integer_part[0] == '-':
        is_neg = True
        integer_part = integer_part[1:]
    else:
        is_neg = False

    result = 0

    integer_part = integer_part[::-1]
    for i in range(len(integer_part)):
        result += int(integer_part[i]) * (4 ** i)

    for i in range(len(fractional_part)):
        result += int(fractional_part[i]) * (4 ** -(i + 1))

    if is_neg:
        result *= -1

    entry_base10.delete(0, tk.END)
    entry_base10.insert(0, str(result))
    entry_base4.delete(0, tk.END)

def convert_10_to_4():
    num = float(entry_base10.get())

    is_neg = num < 0
    num = abs(num)

    integer_part = int(num)
    fractional_part = num - integer_part

    integer_base4 = ''
    if integer_part == 0:
        integer_base4 = '0'
    while integer_part > 0:
        integer_base4 += str(integer_part % 4)
        integer_part //= 4
    integer_base4 = integer_base4[::-1]

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

    entry_base4.delete(0, tk.END)
    entry_base4.insert(0, result)
    entry_base10.delete(0, tk.END)

def clear():
    entry_base10.delete(0, tk.END)
    entry_base4.delete(0, tk.END)

root = tk.Tk()
root.title('Перевод из 10 в 4')
root.geometry('350x350')
root.minsize(350, 350)

label1 = ttk.Label(text = 'Ввод в 4 системе:')
label1.pack()
entry_base4 = ttk.Entry(justify='right', font = 'helvetica 20')
entry_base4.pack()
label2 = ttk.Label(text = 'Ввод в 10 системе:')
label2.pack()
entry_base10 = ttk.Entry(justify='right', font = 'helvetica 20')
entry_base10.pack()

convert_4_to_10 = ttk.Button(text = 'Перевести из 4 в 10', command = convert_4_to_10)
convert_4_to_10.pack()
convert_10_to_4 = ttk.Button(text = 'Перевести из 10 d 4', command = convert_10_to_4)
convert_10_to_4.pack()

clear = ttk.Button(text = "Clear", command = clear)
clear.pack()

root.mainloop()

