import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

SAFE_ENV = {
    "sin": np.sin,
    "cos": np.cos,
    "tan": np.tan,
    "exp": np.exp,
    "log": np.log,
    "sqrt": np.sqrt,
    "pi": np.pi,
    "e": np.e,
    "abs": np.abs,
    "np": np,
    "math": math,
}

def f_from_string(expr):
    def f(x):
        return eval(expr, {"__builtins__": {}}, {**SAFE_ENV, "x": x})
    return f

def derivative(f, x, dx=1e-6):
    return (f(x + dx) - f(x - dx)) / (2 * dx)

def second_derivative(f, x, dx=1e-4):
    return (f(x + dx) - 2 * f(x) + f(x - dx)) / (dx * dx)

def combined_method(f, a, b, eps=1e-6, nmax=100):
    fa, fb = f(a), f(b)
    if fa * fb > 0:
        return None, None, 0, 1

    d2a = second_derivative(f, a)
    d2b = second_derivative(f, b)

    if fa * d2a > 0:
        x_newton = a
        x_chord = b
    elif fb * d2b > 0:
        x_newton = b
        x_chord = a
    else:
        x_newton = a
        x_chord = b

    for it in range(1, nmax + 1):
        dfx = derivative(f, x_newton)
        if abs(dfx) < 1e-12:
            return None, None, it, 2

        f_newton = f(x_newton)
        x_newton_next = x_newton - f_newton / dfx

        f_chord = f(x_chord)
        denom = f_chord - f_newton
        if abs(denom) < 1e-12:
            return None, None, it, 3

        x_chord_next = x_chord - f_chord * (x_chord - x_newton) / denom

        if abs(x_newton_next - x_chord_next) < eps:
            root = (x_newton_next + x_chord_next) / 2
            return root, f(root), it, 0

        x_newton, x_chord = x_newton_next, x_chord_next

    root = (x_newton + x_chord) / 2
    return root, f(root), nmax, 4

def find_intervals(f, a, b, h):
    intervals = []
    x = a
    while x < b:
        x2 = min(x + h, b)
        try:
            y1 = f(x)
            y2 = f(x2)
            if np.isfinite(y1) and np.isfinite(y2) and (y1 == 0 or y1 * y2 < 0):
                intervals.append((x, x2))
        except:
            pass
        x = x2
    return intervals

def find_extrema_points(f, a, b, n=1000):
    xs = np.linspace(a, b, n)
    pts = []
    for i in range(1, len(xs) - 1):
        x = xs[i]
        try:
            d1l = derivative(f, xs[i - 1])
            d1r = derivative(f, xs[i + 1])
            if np.isfinite(d1l) and np.isfinite(d1r):
                if d1l * d1r < 0:
                    pts.append(x)
        except:
            pass
    return pts
def find_inflection_points(f, a, b, n=800):
    xs = np.linspace(a, b, n)
    pts = []
    d2_values = []
    for x in xs:
        try:
            d2 = second_derivative(f, x)
            if np.isfinite(d2):
                d2_values.append(d2)
            else:
                d2_values.append(None)
        except:
            d2_values.append(None)

    for i in range(1, len(xs) - 1):
        left = d2_values[i - 1]
        right = d2_values[i + 1]
        if left is None or right is None:
            continue
        if left * right < 0:
            pts.append(xs[i])
    return pts

def format_scientific_one_digit(v):
    if v == 0:
        return "0.0e+00"
    return "{:.1e}".format(v)

def analyze_and_plot():
    try:
        expr = entry_func.get().strip()
        a = float(entry_a.get())
        b = float(entry_b.get())
        h = float(entry_h.get())
        eps = float(entry_eps.get())
        nmax = int(entry_nmax.get())
        f = f_from_string(expr)
    except Exception as e:
        messagebox.showerror("Ошибка", f"Неверный ввод: {e}")
        return

    if a >= b:
        messagebox.showerror("Ошибка", "Должно быть a < b")
        return
    if h <= 0 or eps <= 0 or nmax <= 0:
        messagebox.showerror("Ошибка", "h, eps и Nmax должны быть положительными")
        return

    intervals = find_intervals(f, a, b, h)
    rows = []

    for i, (x1, x2) in enumerate(intervals, start=1):
        root, fr, iters, code = combined_method(f, x1, x2, eps, nmax)
        if code == 0:
            rows.append([
                i,
                f"[{x1:.6g}; {x2:.6g}]",
                f"{root:.10f}",
                format_scientific_one_digit(fr),
                iters,
                code
            ])

    for item in tree.get_children():
        tree.delete(item)
    for row in rows:
        tree.insert("", "end", values=row)

    ax.clear()
    xs = np.linspace(a, b, 2000)
    ys = []
    for x in xs:
        try:
            y = f(x)
            ys.append(y if np.isfinite(y) else np.nan)
        except:
            ys.append(np.nan)
    ys = np.array(ys, dtype=float)

    ax.plot(xs, ys, label="f(x)")
    ax.axhline(0, color="black", linewidth=1)

    roots = [float(r[2]) for r in rows]
    if roots:
        ax.scatter(roots, [0] * len(roots), color="red", zorder=5, label="roots")

    exts_x = find_extrema_points(f, a, b)
    infl_x = find_inflection_points(f, a, b)

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
            ax.scatter(exts_x2, exts_y, color="green", s=25, label="extrema")

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
            ax.scatter(infl_x2, infl_y, color="purple", s=25, label="inflection")

    ax.set_xlim(a, b)
    ax.grid(True)
    ax.legend()
    canvas.draw()




root = tk.Tk()
root.title("ЛР №2 — Метод комбинированный")

frm = ttk.Frame(root, padding=10)
frm.pack(side=tk.LEFT, fill=tk.Y)

labels = ["f(x) =", "a =", "b =", "h =", "eps =", "Nmax ="]
defaults = ["sin(x)", "-5", "5", "0.5", "1e-6", "100"]

entries = []
for i, (lab, val) in enumerate(zip(labels, defaults)):
    ttk.Label(frm, text=lab).grid(row=i, column=0, sticky="w", pady=2)
    e = ttk.Entry(frm, width=25)
    e.insert(0, val)
    e.grid(row=i, column=1, pady=2)
    entries.append(e)

entry_func, entry_a, entry_b, entry_h, entry_eps, entry_nmax = entries

btn = ttk.Button(frm, text="Вычислить", command=analyze_and_plot)
btn.grid(row=6, column=0, columnspan=2, pady=10, sticky="we")

tree = ttk.Treeview(frm, columns=("n", "interval", "root", "froot", "iters", "code"), show="headings", height=12)
for col, text, width in [
    ("n", "№", 40),
    ("interval", "[xi;xi+1]", 110),
    ("root", "x'", 110),
    ("froot", "f(x')", 100),
    ("iters", "Итераций", 80),
    ("code", "Код", 50),
]:
    tree.heading(col, text=text)
    tree.column(col, width=width, anchor="center")
tree.grid(row=7, column=0, columnspan=2, pady=5)

plot_frame = ttk.Frame(root)
plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

fig, ax = plt.subplots(figsize=(8, 5), dpi=100)
canvas = FigureCanvasTkAgg(fig, master=plot_frame)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
canvas.draw()

root.mainloop()