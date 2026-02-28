# Вариант 13 (Сложение и вычитание чисел в 4 системе счисления)

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
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

def show_info():
    messagebox.showinfo('Информация', 'Автор: Макжанов Илья\n'
                                      'Калькулятор в 4 системе счисления')

#Создание окна
root = tk.Tk()
root.title('Калькулятор в 4 системе счисления')
root.geometry('350x350')
# Задаем минимальный размер окна
root.minsize(350, 350)

# Добавление стиля
ttk.Style().configure(".",  font="helvetica 20", foreground="#1144AA", background="#79A3F5")

# Создание меню
main_menu = tk.Menu(root)
root.config(menu=main_menu)

main_menu.add_command(label = 'Посчитать', command = procedure)
main_menu.add_command(label = 'Информация', command = show_info)

clear_menu = tk.Menu(main_menu, tearoff = False)
clear_menu.add_command(label = 'Очистить всё', command = clearAll)
clear_menu.add_command(label = 'Удалить последний символ', command = backspace)
main_menu.add_cascade(label = 'Очистка', menu = clear_menu)

# Позиционирование с помощью Grid (сетка из 4 столбцов и 4 строк)
for c in range(4): root.columnconfigure(index = c, weight = 1)
for r in range(4): root.rowconfigure(index = r, weight = 1)

# Создание кнопок и полей ввода
inputEntry = ttk.Entry(justify='right', font = 'helvetica 26')
inputEntry.grid(column = 0, row = 0, columnspan = 4, sticky ='nsew')

# Кнопки удаления
clearAllBtn = ttk.Button(text = 'Очистить всё', command = clearAll)
clearAllBtn.grid(column = 0, row = 1, columnspan = 3, sticky = 'nsew')

clearBtn = ttk.Button(text = '⌫', command = backspace)
clearBtn.grid(column = 3, row = 1, sticky = 'nsew')

# Кнопки цифр
btn_0 = ttk.Button(text = '0', command = lambda: add('0'))
btn_0.grid(column = 0, row = 2, sticky = 'nsew')

btn_1 = ttk.Button(text = '1', command = lambda: add('1'))
btn_1.grid(column = 1, row = 2, sticky = 'nsew')

btn_2 = ttk.Button(text = '2', command = lambda: add('2'))
btn_2.grid(column = 0, row = 3, sticky = 'nsew')

btn_3 = ttk.Button(text = '3', command = lambda: add('3'))
btn_3.grid(column = 1, row = 3, sticky = 'nsew')

# Кнопки операций
dot_btn = ttk.Button(text ='.', command = lambda: add('.'))
dot_btn.grid(column = 2, row = 3, sticky ='nsew')

plus_btn = ttk.Button(text ='+', command = lambda: add('+'))
plus_btn.grid(column = 2, row = 2, sticky = 'nsew')

minus_btn = ttk.Button(text = '-', command = lambda: add('-'))
minus_btn.grid(column = 3, row = 2, sticky = 'nsew')

equal_btn = ttk.Button(text = '=', command = procedure)
equal_btn.grid(column = 3, row = 3, sticky = 'nsew')

root.mainloop()

