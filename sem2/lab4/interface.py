import tkinter as tk
from tkinter import messagebox, ttk

from functions import *


# Функции интерфейса

def add_point_from_canvas(event):
    "считывает координаты нажатия на холст и добавляет точку в список всех точек"
    points.append((event.x, event.y))
    draw_point(event.x, event.y)
    add_point_to_text()

def add_point_from_button():
    "добавляет точку по кнопке"
    x = x_entry.get()
    y = y_entry.get()
    try:
        x, y = int(x), int(y)
    except:
        messagebox.showerror("Ошибка", "Координаты точки должны быть целыми числами")
        return
    points.append((x, y))
    draw_point(x, y)
    add_point_to_text()


def draw_point(x, y):
    "рисует точку на холсте"
    canvas.create_oval(x - 2, y - 2, x + 2, y + 2, fill="black")


def add_point_to_text():
    "добавляет точку в listBox"
    ind = len(points) - 1
    points_list.insert(tk.END, f"{ind + 1}. X: {points[ind][0]}; Y: {points[ind][1]}")
    points_list.see(tk.END)

def clear_all():
    "очищает список точек и холст"
    clear_solution()
    canvas.delete("all")
    points.clear()
    points_list.delete(0, tk.END)

def clear_solution():
    canvas.delete("solution")
    solution_label.config(text = "")

def solve():
    clear_solution()
    if len(points) < 2:
        messagebox.showerror("Ошибка", "Должно быть как минимум 2 точки")
        return
    try:
        radius = int(radius_entry.get())
    except:
        messagebox.showerror("Ошибка", "Радиус должен быть целым числом")
        return
    a, b, included_points = find_points(points, radius)
    canvas.create_oval(
        a[0] - radius, a[1] - radius,
        a[0] + radius, a[1] + radius,
        outline='blue', tags = 'solution')
    canvas.create_oval(
        b[0] - radius, b[1] - radius,
        b[0] + radius, b[1] + radius,
        outline='red', tags = 'solution')
    # запись в текстовое поле
    solution_label.config(text = f"1: X: {a[0]}; Y: {a[1]}\n2: X: {b[0]}; Y: {b[1]}\n Точек внутри: {included_points}")


points = []

root = tk.Tk()
root.geometry("800x600")
root.minsize(800, 600)
root.title("Лабораторная работа 4")

# создание сетки
for c in range(8): root.columnconfigure(index=c, weight=1)
for r in range(20): root.rowconfigure(index=r, weight=1)

# расположение элементов
canvas = tk.Canvas(root)
canvas.grid(row=0, column=2, rowspan=20, columnspan=6, sticky='nsew')
canvas.bind("<Button-1>", add_point_from_canvas)

ttk.Label(root, text='X:').grid(row=0, column=0)
ttk.Label(root, text='Y:').grid(row=1, column=0)

x_entry = ttk.Entry(root)
x_entry.grid(row=0, column=1)
y_entry = ttk.Entry(root)
y_entry.grid(row=1, column=1)

add_point_btn = ttk.Button(root, text='Добавить точку', command=add_point_from_button)
add_point_btn.grid(row=2, column=0, columnspan=2)

# список всех точек
points_list = tk.Listbox(root)
points_list.grid(row=3, column=0, columnspan=2, rowspan=10, sticky="nsew")

# радиус
ttk.Label(root, text="Радиус:").grid(row=13, column=0)
radius_entry = ttk.Entry(root)
radius_entry.insert(0, "100")
radius_entry.grid(row=13, column=1)

# кнопки очистки
clear_all_btn = ttk.Button(root, text="Очистить все", command=clear_all)
clear_all_btn.grid(row=14, column=0, columnspan=2)


clear_solution_btn = ttk.Button(root, text = "Очистить решение", command = clear_solution)
clear_solution_btn.grid(row=15, column=0, columnspan=2)

# кнопка решения
solve_btn = ttk.Button(root, text="Решить", command=solve)
solve_btn.grid(row=16, column=0, columnspan=2)

# вывод решения
ttk.Label(root, text = "Решение:").grid(row=17, column=0)
solution_label = ttk.Label(root)
solution_label.grid(row=18, column=0, columnspan=2)


root.mainloop()
