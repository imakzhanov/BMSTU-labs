import tkinter as tk
from tkinter import ttk
from functions import *

root = tk.Tk()
root.geometry("400x200")
root.minsize(400, 200)

# ---------Создание Сетки -----------------
for c in range(2): root.columnconfigure(index=c, weight=1)
for r in range(4): root.rowconfigure(index=r, weight=1)

# --------- Создание кнопок, поля ввода и поля вывода --------------------

ttk.Label(root, text='Введите сообщение:').grid(column=0, row=0)
message_entry = ttk.Entry(root)
message_entry.grid(column=1, row=0, sticky='ew')

hide_btn = ttk.Button(root, text='Скрыть сообщение', command=lambda: hide_message(message_entry.get()))
hide_btn.grid(column=0, row=1, columnspan=2)

pull_btn = ttk.Button(root, text='Извлечь сообщение', command=lambda: get_message(message_label))
pull_btn.grid(column=0, row=2, columnspan=2)

ttk.Label(root, text='Полученное сообщение:').grid(column=0, row=3)
message_label = ttk.Label(root)
message_label.grid(column=1, row=3, sticky='ew')



root.mainloop()
