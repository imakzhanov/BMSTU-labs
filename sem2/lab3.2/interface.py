import tkinter as tk
from tkinter import ttk
from functions import *


def get_data_and_create():
    width = width_entry.get()
    height = height_entry.get()
    capacity = capacity_entry.get()
    if (width.isdigit() and height.isdigit() and capacity.isdigit() and
        0 < int(width) <= 10000 and 0 < int(height) <= 10000 and 0 < int(capacity) <= 5000):
        create_img(int(width), int(height), int(capacity))
    else:
        messagebox.showerror("Ошибка", "Введены не числа, или они превышают границы")

def get_data_and_classify():
    k = k_entry.get()
    if (k.isdigit() and int(k) > 0):
        classify_img(int(k))
    else:
        messagebox.showerror("Ошибка", "Введены не числа, или они превышают границы")

# -----------Создание окна --------------
root = tk.Tk()
root.geometry("400x200")
root.minsize(400, 200)

# ---------Создание Сетки -----------------
for c in range(2): root.columnconfigure(index=c, weight=1)
for r in range(6): root.rowconfigure(index=r, weight=1)

# --------- Создание кнопок, поля ввода и поля вывода --------------------

labels = ["Ширина изображения:", "Высота изображения:", "Мощность множества:"]

entries_defaults = ["150", "200", "1000", "10"]
entries = []
for i in range(3):
    ttk.Label(text=labels[i]).grid(column=0, row=i)
    e = ttk.Entry(root)
    e.insert(0, entries_defaults[i])
    e.grid(column=1, row=i)
    entries.append(e)

width_entry, height_entry, capacity_entry = entries

create_btn = ttk.Button(root, text="Создать изображение", command=get_data_and_create)
create_btn.grid(column=0,row=3, columnspan=2)

ttk.Label(text="Количество ближайших соседей").grid(column=0, row=4)
k_entry = ttk.Entry(root)
k_entry.insert(0, entries_defaults[3])
k_entry.grid(column=1, row=4)

classify_btn = ttk.Button(root, text="Классифицировать точки", command=get_data_and_classify)
classify_btn.grid(column=0,row=5, columnspan=2)


root.mainloop()