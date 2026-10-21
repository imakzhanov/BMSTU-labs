import numpy as np
from sklearn.metrics import adjusted_rand_score, normalized_mutual_info_score, silhouette_score
from distances import pairwise_distance


def elbow_point(ks, values):
    """
    Метод локтя: поиск точки с максимальным расстоянием до прямой
    между первой и последней точками нормированного графика.
    """
    ks = np.asarray(ks, dtype=float)
    values = np.asarray(values, dtype=float)
    # Нормировка в [0, 1]
    ks_norm = (ks - ks[0]) / (ks[-1] - ks[0])
    v_min, v_max = np.min(values), np.max(values)
    if v_max == v_min:
        return int(ks[0])          # кривая плоская - локтя нет
    vs_norm = (values - v_min) / (v_max - v_min)

    # Прямая между первой и последней точкой
    p1 = np.array([ks_norm[0], vs_norm[0]])
    p2 = np.array([ks_norm[-1], vs_norm[-1]])

    # Расстояние от точки (x0, y0) до прямой Ax + By + C = 0
    # Прямая через две точки: (y2-y1)x - (x2-x1)y + x2y1 - y2x1 = 0
    A = p2[1] - p1[1]
    B = p1[0] - p2[0]
    C = p2[0] * p1[1] - p2[1] * p1[0]

    distances = np.abs(A * ks_norm + B * vs_norm + C) / np.sqrt(A ** 2 + B ** 2)
    return int(ks[np.argmax(distances)])


def external_metrics(true_labels, pred_labels):
    """Вычисляет ARI, NMI и Purity."""
    true_labels = np.asarray(true_labels)
    pred_labels = np.asarray(pred_labels)
    ari = adjusted_rand_score(true_labels, pred_labels)
    nmi = normalized_mutual_info_score(true_labels, pred_labels)

    # Purity: для каждого кластера находим самый частый истинный класс
    purity_sum = 0
    clusters = np.unique(pred_labels)
    for c in clusters:
        indices = np.where(pred_labels == c)[0]
        if len(indices) == 0:
            continue
        # Считаем распределение истинных меток в этом кластере
        true_in_cluster = true_labels[indices]
        counts = np.bincount(true_in_cluster)
        purity_sum += np.max(counts)

    purity = purity_sum / len(true_labels)

    return {"ARI": ari, "NMI": nmi, "purity": purity}


def silhouette(X, labels, measure):
    """Коэффициент силуэта на основе матрицы расстояний выбранной меры."""
    if len(np.unique(labels)) < 2:
        return np.nan
    dist_matrix = pairwise_distance(X, X, measure)
    # Для precomputed нужна симметричная матрица с нулевой диагональю
    dist_matrix = (dist_matrix + dist_matrix.T) / 2.0
    np.fill_diagonal(dist_matrix, 0.0)
    return float(silhouette_score(dist_matrix, labels, metric="precomputed"))
