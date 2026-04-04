import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
import numpy as np
from functions import *


def calculate_and_plot():
    try:
        expr = func_entry.get().strip()
        a = float(a_entry.get())
        b = float(b_entry.get())
        h = float(h_entry.get())
        eps = float(eps_entry.get())
        nmax = int(nmax_entry.get())
        f = get_function(expr)
    except Exception as e:
        messagebox.showerror("Ошибка", f"Неверный ввод: {e}")
        return
    if a >= b:
        messagebox.showerror("Ошибка", "Должно быть a < b")
        return
    if h <= 0 or eps <= 0 or nmax <= 0:
        messagebox.showerror("Ошибка", "h, eps и Nmax должны быть положительными")
        return

    intervals = get_intervals(f, a, b, h)
    table_rows = []
    roots = []

    for i, (x1, x2) in enumerate(intervals, start=1):
        root, f_root, iters, code = combinend_method(f, x1, x2, eps, nmax)

        if code == 0:
            roots.append(root)
            table_rows.append([
                i,
                f"[{x1:.6g}; {x2:.6g}]",
                f"{root:.10f}",
                "0.0e+00" if f_root == 0 else "{:.1e}".format(f_root),
                iters,
                code
            ])

    clear_table()

    for row in table_rows:
        add_row_to_table(row)


    create_plot(f, a, b)

    if roots:
        plt.scatter(roots, [0] * len(roots), color="red", zorder=5, label="roots")

    exts_x = get_extremum_points(f, a, b)
    infl_x = get_inflection_points(f, a, b)

    if exts_x:
        exts_y = []
        exts_x2 = []
        for x in exts_x:
            try:
                y = f(x)
                if np.isfinite(y):
                    exts_x2.append(x)
                    exts_y.append(y)
            except:
                pass
        if exts_x2:
            plt.scatter(exts_x2, exts_y, color="green", s=25, label="точки экстремума")


    if infl_x:
        infl_y = []
        infl_x2 = []
        for x in infl_x:
            try:
                y = f(x)
                if np.isfinite(y):
                    infl_x2.append(x)
                    infl_y.append(y)
            except:
                pass
        if infl_x2:
            plt.scatter(infl_x2, infl_y, color="blue", s=25, label="точки перегиба")

    plt.grid(True)
    plt.legend(loc='upper right')

    plt.show()


# ===============ФУНКЦИИ ДЛЯ ТАБЛИЦЫ===============
def create_table(root):
    columns = ("№", "Отрезок", "x`", "f(x`)", "Итераций", "Код ошибки")

    table = ttk.Treeview(root, columns=columns, show="headings", height=10)

    for col in columns:
        table.heading(col, text=col)
        table.column(col, width=100)

    table.grid(row=7, column=0, columnspan=2)

    return table


def clear_table():
    for item in table.get_children():
        table.delete(item)


def add_row_to_table(values):
    table.insert("", "end", values=values)


# ===============ФУНКЦИИ ДЛЯ ГРАФИКА===============
def create_plot(f, a, b, n=1000):
    xs = np.linspace(a, b, n)
    ys = []
    for x in xs:
        try:
            y = f(x)
            ys.append(y if np.isfinite(y) else np.nan)
        except:
            ys.append(np.nan)
    ys = np.array(ys, dtype=float)

    plt.clf()
    plt.axhline(y=0, color='black', linewidth=1)
    plt.axvline(x=0, color='black', linewidth=1)

    plt.plot(xs, ys)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("График функции y = f(x)")
    plt.grid(True)




root = tk.Tk()
root.title("Поиск корней комбинированным методом")
root.geometry('600x500')
root.minsize(600, 500)

# создаем Grid
for c in range(2): root.columnconfigure(index=c, weight=1)
for r in range(10): root.rowconfigure(index=r, weight=1)

labels = ["f(x):", "a:", "b:", "h:", "eps:", "Nmax:"]

defaults = ["sin(x)", "-10", "10", "0.5", "1e-6", "100"]

entries = []

for i, name in enumerate(labels):
    ttk.Label(root, text=name).grid(row=i, column=0, sticky="nsew", pady=2)
    e = ttk.Entry(root, width=25)
    e.insert(0, defaults[i])
    e.grid(row=i, column=1, pady=2)
    entries.append(e)

func_entry, a_entry, b_entry, h_entry, eps_entry, nmax_entry = entries

btn = ttk.Button(root, text="Вычислить", command=calculate_and_plot)
btn.grid(row=6, column=0, columnspan=2, pady=10, sticky="we")

table = create_table(root)

root.mainloop()
