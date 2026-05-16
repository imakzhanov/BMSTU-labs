import tkinter as tk
from tkinter import ttk
from functions import *

root = tk.Tk()
root.geometry("700x300")
root.minsize(700, 300)

#  Создание Сетки
for c in range(4): root.columnconfigure(index=c, weight=1)
for r in range(6): root.rowconfigure(index=r, weight=1)

# Создание кнопок, поля ввода и поля вывода

ttk.Label(root, text='Введите сообщение:').grid(column=0, row=0)
message_entry = ttk.Entry(root)
message_entry.grid(column=1, row=0, sticky='ew', columnspan=2)

ttk.Label(root, text='Скрыть:').grid(column=0, row=1)
image_path = ttk.Entry(root)
image_path.grid(column=1, row=1, sticky='ew')
choose_img_path = ttk.Button(root, text="Выбрать", command=lambda: open_file(image_path))
choose_img_path.grid(column=2, row=1, sticky='ew')

open_img = ttk.Button(text="Открыть", command=lambda: show_image(image_path.get()))
open_img.grid(column=3, row=1, sticky='ew')


hide_btn = ttk.Button(root, text='Скрыть сообщение',
                      command=lambda: hide_message(image_path.get(), message_entry.get()))
hide_btn.grid(column=0, row=2, columnspan=3)

ttk.Label(root, text='Извлечь:').grid(column=0, row=3)
res_path = ttk.Entry(root)
res_path.grid(column=1, row=3, sticky='ew')
choose_res_path = ttk.Button(root, text="Выбрать", command=lambda: open_file(res_path))
choose_res_path.grid(column=2, row=3, sticky='ew')

open_res = ttk.Button(text="Открыть", command=lambda: show_image(res_path.get()))
open_res.grid(column=3, row=3, sticky='ew')


pull_btn = ttk.Button(root, text='Извлечь сообщение',
                      command=lambda: get_message(res_path.get(), message_label))
pull_btn.grid(column=0, row=4, columnspan=3)

ttk.Label(root, text='Полученное сообщение:').grid(column=0, row=5)
message_label = ttk.Label(root)
message_label.grid(column=1, row=5, sticky='ew', columnspan=2)


root.mainloop()
