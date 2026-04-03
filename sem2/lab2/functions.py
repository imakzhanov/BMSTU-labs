from math import *
import numpy as np


def get_function(str):
    def f(x):
        return eval(str)

    return f


# returns derivative value
def derivative(f, x, dx=1e-6):
    deriv = (f(x + dx) - f(x)) / dx
    return deriv


def second_derivative(f, x, dx=1e-6):
    second_deriv = (f(x + dx) - 2 * f(x) - f(x - dx)) / dx ** 2
    return second_deriv


def combinend_method(f, a, b, eps=1e-6, nmax=100):
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

    for i in range(1, nmax + 1):
        # метод Ньютона (касательных)
        dfx = derivative(f, x_newton)
        if abs(dfx) < eps:
            return None, None, i, 2
        f_newton = f(x_newton)
        x_newton_next = x_newton - f_newton / dfx

        # метод хорд
        f_chord = f(x_chord)
        if abs(f_chord - f_newton) < eps:
            return None, None, i, 3
        x_chord_next = x_chord - f_chord * (x_chord - x_newton) / (f_chord - f_newton)

        x_newton, x_chord = x_newton_next, x_chord_next

        if abs(x_newton - x_chord) < eps:
            root = (x_newton + x_chord) / 2
            return root, f(root), i, 0

    root = (x_newton + x_chord) / 2
    return root, f(root), nmax, 2


# находит все интервалы с корнями
def get_intervals(f, a, b, h):
    intervals = []
    x1 = a
    while x1 < b:
        x2 = min(x1 + h, b)
        try:
            y1, y2 = f(x1), f(x2)
            if np.isfinite(y1) and np.isfinite(y2) and (y1 == 0 or y1 * y2 < 0):
                intervals.append((x1, x2))
        except:
            pass
        x1 = x2
    return intervals


# находит все точки экстремума
def get_extremum_points(f, a, b, n=500):
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


# находит все точки перегиба
def get_inflection_points(f, a, b, n=800):
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
