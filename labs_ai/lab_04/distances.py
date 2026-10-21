import numpy as np

# Словарь типов мер для отчетов
MEASURES = {
    "euclid": "метрическая",
    "tanimoto": "ассоциативная",
    "pearson": "корреляционная"
}


def pairwise_distance(A, B, measure):
    """
    Вычисляет матрицу расстояний между наборами векторов A и B.
    Результат: np.ndarray формы [len(A), len(B)]
    """
    if measure == "euclid":
        # Евклидово расстояние: sqrt(sum((x-y)^2))
        # Используем формулу: ||x-y||^2 = ||x||^2 + ||y||^2 - 2*x.y
        a_sq = np.sum(A ** 2, axis=1).reshape(-1, 1)
        b_sq = np.sum(B ** 2, axis=1).reshape(1, -1)
        dist_sq = a_sq + b_sq - 2 * np.dot(A, B.T)
        # Защита от отрицательных значений из-за точности float
        return np.sqrt(np.maximum(dist_sq, 0))

    elif measure == "tanimoto":
        # Коэффициент Танимото: s = (x.y) / (|x|^2 + |y|^2 - x.y)
        # Расстояние d = 1 - s
        dot_product = np.dot(A, B.T)
        a_sq = np.sum(A ** 2, axis=1).reshape(-1, 1)
        b_sq = np.sum(B ** 2, axis=1).reshape(1, -1)
        denom = a_sq + b_sq - dot_product

        # Защита от деления на 0 (если оба вектора нулевые, s=0, d=1)
        s = np.divide(dot_product, denom, out=np.zeros_like(dot_product), where=denom != 0)
        # Расстояние не может быть отрицательным (погрешность float)
        return np.maximum(1.0 - s, 0.0)

    elif measure == "pearson":
        # Коэффициент Пирсона: r = cov(x, y) / (std(x) * std(y))
        # Расстояние d = 1 - r
        # Центрирование данных (вычитаем среднее по строкам)
        A_centered = A - np.mean(A, axis=1, keepdims=True)
        B_centered = B - np.mean(B, axis=1, keepdims=True)

        # Нормировка на L2-норму (стандартное отклонение * sqrt(n))
        a_norm = np.linalg.norm(A_centered, axis=1, keepdims=True)
        b_norm = np.linalg.norm(B_centered, axis=1, keepdims=True)

        # Защита от нулевого стандартного отклонения
        A_normed = np.divide(A_centered, a_norm, out=np.zeros_like(A_centered), where=a_norm != 0)
        B_normed = np.divide(B_centered, b_norm, out=np.zeros_like(B_centered), where=b_norm != 0)

        # Матричное умножение нормированных векторов дает корреляцию r
        r = np.dot(A_normed, B_normed.T)
        # r лежит в [-1; 1], d = 1 - r в [0; 2] (обрезаем погрешность float)
        return np.clip(1.0 - r, 0.0, 2.0)

    else:
        raise ValueError(f"Unknown measure: {measure}")
