import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import numpy as np


def func(str):
    def f(x):
        return eval(str)
    return f

def calc():
    a_value = float(a.get())
    b_value = float(b.get())
    c_value = float(c.get())

    f = func(f"{a_value}*x**2 + {b_value}*x + {c_value}")

    xs = np.linspace(-10, 10, 200)
    ys = []
    for x in xs:
        ys.append(f(x))

    plt.clf()

    plt.plot(xs, ys)

    plt.grid(True)
    plt.axhline(y=0)
    plt.axvline(x=0)
    plt.show()


root = tk.Tk()
root.geometry('300x300')

a = ttk.Entry(root)
b = ttk.Entry(root)
c = ttk.Entry(root)

a.pack()
b.pack()
c.pack()

btn = ttk.Button(root, text="Построить", command=calc)
btn.pack()

root.mainloop()
