from math import *
import numpy as np


def get_function(str):
    def f(x):
        return eval(str)

    return f


# returns derivative func
def get_derivative(f, dx = 1e-6):
    def deriv(x):
        return (f(x + dx) - f(x)) / dx
    return deriv


def get_second_derivative(f, dx=1e-6):
    def second_deriv(x):
        return (f(x + dx) - 2 * f(x) - f(x - dx)) / dx ** 2
    return second_deriv


def combinend_method(f, a, b, eps=1e-6, nmax=100):
    fa, fb = f(a), f(b)
    if fa * fb > 0:
        return None, None, 0, 1

    sec_deriv = get_second_derivative(f, eps)
    d2a = sec_deriv(a)
    d2b = sec_deriv(b)

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
        deriv = get_derivative(f)
        dfx = deriv(x_newton)
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
    return root, f(root), nmax, 4


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
def get_extremum_intervals(f, a, b, h):
    intervals = []
    x1 = a
    deriv = get_derivative(f)
    while x1 < b:
        x2 = min(x1 + h, b)
        try:
            y1, y2 = deriv(x1), deriv(x2)
            if np.isfinite(y1) and np.isfinite(y2) and (y1 == 0 or y1 * y2 < 0):
                intervals.append((x1, x2))
        except:
            pass
        x1 = x2
    return intervals


# находит все точки перегиба
def get_inflection_intervals(f, a, b, h):
    intervals = []
    x1 = a
    sec_deriv = get_second_derivative(f)

    while x1 < b:
        x2 = min(x1 + h, b)
        try:
            y1, y2 = sec_deriv(x1), sec_deriv(x2)
            if np.isfinite(y1) and np.isfinite(y2) and (y1 == 0 or y1 * y2 < 0):
                intervals.append((x1, x2))
        except:
            pass
        x1 = x2
    return intervals
