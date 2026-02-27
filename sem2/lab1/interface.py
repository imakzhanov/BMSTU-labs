# Вариант 13 (Сложение и вычитание чисел в 4 системе счисления)

import tkinter as tk
from tkinter import ttk
from functions import *


# добавление символа
def add(char):
    inputEntry.insert(tk.END, char)

# очистка поля
def clearAll():
    inputEntry.delete(0, tk.END)

# очистка последнего символа
def backspace():
    value = inputEntry.get()
    clearAll()
    inputEntry.insert(0, value[:-1])

def procedure():
    result = calculate(inputEntry.get())
    clearAll()
    inputEntry.insert(0, result)


root = tk.Tk()
root.title('Калькулятор в 4 системе счисления')
root.geometry('350x350')
# Задаем минимальный размер окна
root.minsize(350, 350)


# Позиционирование с помощью Grid (сетка из 4 столбцов и 5 строк)
for c in range(4): root.columnconfigure(index = c, weight = 1)
for r in range(4): root.rowconfigure(index = r, weight = 1)

# Создание кнопок и полей ввода
inputEntry = ttk.Entry(justify='right')
inputEntry.grid(column = 0, row = 0, columnspan = 4, sticky ='nsew')

# Кнопки удаления
clearAllBtn = ttk.Button(text = 'Очистить всё', command = clearAll)
clearAllBtn.grid(column = 0, row = 1, columnspan = 3, sticky = 'nsew')

clearBtn = ttk.Button(text = '<', command = backspace)
clearBtn.grid(column = 3, row = 1, sticky = 'nsew')

# Кнопки цифр
btn_0 = ttk.Button(text = '0', command = lambda x = '0': add(x))
btn_0.grid(column = 0, row = 2, sticky = 'nsew')

btn_1 = ttk.Button(text = '1', command = lambda x = '1': add(x))
btn_1.grid(column = 1, row = 2, sticky = 'nsew')

btn_2 = ttk.Button(text = '2', command = lambda x = '2': add(x))
btn_2.grid(column = 0, row = 3, sticky = 'nsew')

btn_3 = ttk.Button(text = '3', command = lambda x = '3': add(x))
btn_3.grid(column = 1, row = 3, sticky = 'nsew')

# Кнопки операций
dot_btn = ttk.Button(text =',', command = lambda x ='.': add(x))
dot_btn.grid(column = 2, row = 3, sticky ='nsew')

plus_btn = ttk.Button(text ='+', command = lambda x = '+': add(x))
plus_btn.grid(column = 2, row = 2, sticky = 'nsew')

minus_btn = ttk.Button(text = '-', command = lambda x = '-': add(x))
minus_btn.grid(column = 3, row = 2, sticky = 'nsew')

equal_btn = ttk.Button(text = '=', command = procedure)
equal_btn.grid(column = 3, row = 3, sticky = 'nsew')

root.mainloop()

