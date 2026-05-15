import tkinter as tk
from tkinter import messagebox
import math


# ==========================================
# МОДУЛЬ ВЫЧИСЛЕНИЙ (Логика задачи)
# По требованиям его можно вынести в отдельный файл (например, solver.py)
# ==========================================

def get_distance(p1, p2):
    """Вычисляет расстояние между двумя точками."""
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])


def count_points_in_circle(center, points, radius):
    """Считает количество точек внутри окружности заданного радиуса."""
    count = 0
    for p in points:
        if get_distance(center, p) <= radius:
            count += 1
    return count


def find_solution(points, radius):
    """
    Находит две различные точки, окружности которых содержат
    одинаковое количество точек. (Метод полного перебора).
    Возвращает кортеж: (точка1, точка2, количество_точек) или None.
    """
    n = len(points)
    if n < 2:
        return None

    for i in range(n):
        for j in range(i + 1, n):
            c1 = count_points_in_circle(points[i], points, radius)
            c2 = count_points_in_circle(points[j], points, radius)

            if c1 == c2:
                return (points[i], points[j], c1)
    return None


# ==========================================
# МОДУЛЬ ИНТЕРФЕЙСА (GUI на Tkinter)
# ==========================================

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Лабораторная работа: Планиметрия")
        self.geometry("900x600")
        self.resizable(False, False)

        self.points = []  # Список кортежей (x, y)
        self.result_data = None  # Хранение текущего результата

        self.setup_ui()

    def setup_ui(self):
        # --- Левая панель (Управление) ---
        control_frame = tk.Frame(self, width=250, padx=10, pady=10)
        control_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Ввод координат
        tk.Label(control_frame, text="Добавить точку с клавиатуры:").pack(anchor=tk.W)
        coord_frame = tk.Frame(control_frame)
        coord_frame.pack(fill=tk.X, pady=5)

        tk.Label(coord_frame, text="X:").pack(side=tk.LEFT)
        self.entry_x = tk.Entry(coord_frame, width=5)
        self.entry_x.pack(side=tk.LEFT, padx=5)

        tk.Label(coord_frame, text="Y:").pack(side=tk.LEFT)
        self.entry_y = tk.Entry(coord_frame, width=5)
        self.entry_y.pack(side=tk.LEFT, padx=5)

        tk.Button(coord_frame, text="Добавить", command=self.add_point_kb).pack(side=tk.LEFT, padx=5)

        # Список точек
        tk.Label(control_frame, text="Список точек:").pack(anchor=tk.W, pady=(10, 0))
        self.listbox = tk.Listbox(control_frame, height=10)
        self.listbox.pack(fill=tk.X, pady=5)

        # Радиус
        tk.Label(control_frame, text="Радиус окружностей (R):").pack(anchor=tk.W, pady=(10, 0))
        self.entry_r = tk.Entry(control_frame)
        self.entry_r.insert(0, "50")  # Значение по умолчанию
        self.entry_r.pack(fill=tk.X, pady=5)

        # Кнопки управления
        tk.Button(control_frame, text="Решить задачу", bg="lightblue", command=self.solve_task).pack(fill=tk.X, pady=10)
        tk.Button(control_frame, text="Очистить результат", command=self.clear_result).pack(fill=tk.X, pady=2)
        tk.Button(control_frame, text="Очистить всё", fg="red", command=self.clear_all).pack(fill=tk.X, pady=2)

        # Вывод текста результата
        tk.Label(control_frame, text="Результат:").pack(anchor=tk.W, pady=(10, 0))
        self.lbl_result = tk.Label(control_frame, text="Ожидание расчета...", fg="blue", justify=tk.LEFT,
                                   wraplength=230)
        self.lbl_result.pack(anchor=tk.W, fill=tk.X)

        # --- Правая панель (Холст) ---
        self.canvas = tk.Canvas(self, bg="white", cursor="crosshair")
        self.canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.canvas.bind("<Button-1>", self.add_point_mouse)  # Клик левой кнопкой мыши

    def update_views(self):
        """Синхронизирует холст и список точек."""
        # Обновляем Listbox
        self.listbox.delete(0, tk.END)
        for i, (x, y) in enumerate(self.points):
            self.listbox.insert(tk.END, f"{i + 1}. ({x}, {y})")

        # Обновляем Canvas
        self.canvas.delete("all")

        # Отрисовка точек
        for x, y in self.points:
            self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="black")

        # Если есть результат, рисуем окружности и выделяем точки
        if self.result_data:
            p1, p2, r = self.result_data

            # Рисуем окружности
            self.canvas.create_oval(p1[0] - r, p1[1] - r, p1[0] + r, p1[1] + r, outline="green", width=2)
            self.canvas.create_oval(p2[0] - r, p2[1] - r, p2[0] + r, p2[1] + r, outline="blue", width=2)

            # Выделяем точки-центры красным цветом
            self.canvas.create_oval(p1[0] - 4, p1[1] - 4, p1[0] + 4, p1[1] + 4, fill="red")
            self.canvas.create_oval(p2[0] - 4, p2[1] - 4, p2[0] + 4, p2[1] + 4, fill="red")

    def add_point_kb(self):
        """Добавление точки с клавиатуры."""
        try:
            x = float(self.entry_x.get())
            y = float(self.entry_y.get())
            self.points.append((x, y))
            self.clear_result()  # Очищаем старый результат при добавлении новой точки
            self.update_views()
            self.entry_x.delete(0, tk.END)
            self.entry_y.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Ошибка", "Координаты должны быть числами!")

    def add_point_mouse(self, event):
        """Добавление точки кликом мыши по холсту."""
        self.points.append((event.x, event.y))
        self.clear_result()  # Очищаем старый результат
        self.update_views()

    def solve_task(self):
        """Запуск алгоритма решения."""
        if len(self.points) < 2:
            messagebox.showwarning("Внимание", "Добавьте как минимум 2 точки!")
            return

        try:
            r = float(self.entry_r.get())
            if r <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Радиус должен быть положительным числом!")
            return

        # Вызов функции из логического модуля
        res = find_solution(self.points, r)

        if res:
            p1, p2, count = res
            self.result_data = (p1, p2, r)  # Сохраняем для отрисовки
            self.lbl_result.config(
                text=f"Найдено!\nТочка 1: {p1}\nТочка 2: {p2}\nТочек внутри: {count}",
                fg="green"
            )
        else:
            self.result_data = None
            self.lbl_result.config(text="Таких точек не найдено.", fg="red")

        self.update_views()

    def clear_result(self):
        """Очистка только результата вычислений (точки остаются)."""
        self.result_data = None
        self.lbl_result.config(text="Ожидание расчета...", fg="blue")
        self.update_views()

    def clear_all(self):
        """Полная очистка (точек и результата)."""
        self.points.clear()
        self.clear_result()


if __name__ == "__main__":
    app = App()
    app.mainloop()
