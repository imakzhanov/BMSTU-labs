"""
Статистические характеристики вектора.

Вектор рассматривается как выборка x_1..x_n — значения его компонент.
describe(x) возвращает характеристики 1–10 и 13–18, correlations(M) — 11–12.

Обозначения: n — число компонент, x̄ — среднее, s — стандартное отклонение,
x_(1) <= ... <= x_(n) — упорядоченные значения.
"""

import numpy as np
from scipy import stats

PERCENTILES = (5, 25, 75, 95)


def gini(x) -> float:
    """Коэффициент Джини (для неотрицательных x):
    G = (2 * Σ i·x_(i)) / (n * Σ x_i) − (n + 1) / n,   i = 1..n.
    0 — все значения равны, ближе к 1 — вся «масса» в нескольких компонентах."""
    x = np.sort(x)
    n = len(x)
    total = x.sum()
    if n == 0 or total == 0:
        return float("nan")
    i = np.arange(1, n + 1)
    return float(2 * np.sum(i * x) / (n * total) - (n + 1) / n)


def shannon_entropy(x) -> float:
    """Энтропия Шеннона распределения весов, бит:
    p_i = x_i / Σ x_j,   H = −Σ p_i · log2 p_i   (слагаемые с p_i = 0 равны 0)."""
    total = x.sum()
    if total == 0:
        return float("nan")
    p = x[x > 0] / total
    return float(-np.sum(p * np.log2(p)))


def mode(x) -> float:
    """Мода — значение, которое встречается чаще всего (при равенстве — наименьшее)."""
    return float(stats.mode(x, keepdims=False).mode)


def describe(x) -> dict[str, float]:
    x = np.asarray(x, dtype=float)
    n_all = len(x)
    missing = np.isnan(x)
    x = x[~missing]                      # пропуски не участвуют в расчётах
    n = len(x)

    mean = x.mean()
    std = x.std(ddof=1)                  # несмещённая оценка, делитель n − 1
    q = np.percentile(x, PERCENTILES)
    q25, q75 = q[1], q[2]

    result = {
        "n": n_all,
        "среднее": mean,                                     # 1  x̄ = Σx / n
        "медиана": np.median(x),                             # 2
        "мода": mode(x),                                     # 3
        "станд_отклонение": std,                             # 4  s = √(Σ(x−x̄)² / (n−1))
        "дисперсия": x.var(ddof=1),                          # 5  s²
        "размах": x.max() - x.min(),                         # 6  R = max − min
        "IQR": q75 - q25,                                    # 7  Q3 − Q1
        "асимметрия": stats.skew(x),                         # 8  g1 = m3 / m2^(3/2)
        "эксцесс": stats.kurtosis(x),                        # 9  g2 = m4 / m2² − 3
        "пропуски_%": 100 * missing.sum() / n_all,           # 10
        "коэф_вариации": std / mean if mean else np.nan,     # 13 V = s / x̄
    }
    for p, value in zip(PERCENTILES, q):                     # 14
        result[f"P{p:02d}"] = value
    result.update({
        "джини": gini(x),                                    # 15
        "кардинальность": len(np.unique(x)),                 # 16 число различных значений
        "уникальность": len(np.unique(x)) / n,               # 16 доля различных значений
        "плотность": np.count_nonzero(x) / n,                # 17 доля ненулевых компонент
        "энтропия_бит": shannon_entropy(x),                  # 18
    })
    return {k: float(v) for k, v in result.items()}


def correlations(M):
    """11–12: матрицы корреляций между строками M.
    Пирсон:  r = Σ(x−x̄)(y−ȳ) / √(Σ(x−x̄)² · Σ(y−ȳ)²)
    Спирмен: ρ — коэффициент Пирсона, посчитанный по рангам значений
             (одинаковым значениям присваивается средний ранг)."""
    M = np.asarray(M, dtype=float)
    pearson = np.corrcoef(M)
    spearman = stats.spearmanr(M, axis=1).statistic
    if np.ndim(spearman) == 0:           # для двух векторов scipy возвращает число
        spearman = np.array([[1.0, spearman], [spearman, 1.0]])
    return pearson, spearman


def pair_correlation(x, y) -> tuple[float, float]:
    """Корреляции Пирсона и Спирмена для одной пары векторов."""
    return float(stats.pearsonr(x, y).statistic), float(stats.spearmanr(x, y).statistic)
