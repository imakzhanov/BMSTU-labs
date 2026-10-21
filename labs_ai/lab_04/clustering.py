import numpy as np
from distances import pairwise_distance


def kmeans(X, k, measure, n_init=5, max_iter=100, seed=0):
    rng = np.random.default_rng(seed)
    best_res = None
    min_inertia = float('inf')

    for init_run in range(n_init):
        # Инициализация K-means++
        centers = np.empty((k, X.shape[1]))
        centers[0] = X[rng.integers(0, X.shape[0])]
        for i in range(1, k):
            # Расстояние от всех точек до ближайшего из уже выбранных центров
            dists = pairwise_distance(X, centers[:i], measure)
            min_dists = np.min(dists, axis=1)
            # Вероятность выбора пропорциональна d^2
            total = np.sum(min_dists ** 2)
            if total > 0:
                probs = min_dists ** 2 / total
                centers[i] = X[rng.choice(X.shape[0], p=probs)]
            else:
                # все точки совпали с выбранными центрами - берем случайную
                centers[i] = X[rng.integers(0, X.shape[0])]

        labels = np.full(X.shape[0], -1, dtype=int)
        n_iter = 0
        for iteration in range(max_iter):
            n_iter = iteration + 1
            # Шаг назначения: ближайший центр
            dists = pairwise_distance(X, centers, measure)
            new_labels = np.argmin(dists, axis=1)

            if np.array_equal(labels, new_labels):
                break
            labels = new_labels

            # Шаг пересчета центров (среднее арифметическое)
            for j in range(k):
                cluster_pts = X[labels == j]
                if len(cluster_pts) > 0:
                    centers[j] = np.mean(cluster_pts, axis=0)
                else:
                    # Обработка пустого кластера: берем точку, самую далекую от своего центра
                    d_to_own = np.min(pairwise_distance(X, centers, measure), axis=1)
                    idx_far = np.argmax(d_to_own)
                    centers[j] = X[idx_far]
                    labels[idx_far] = j

        # Метки согласуем с итоговыми центрами, инерция: сумма d(x, center)^2
        final_dists = pairwise_distance(X, centers, measure)
        labels = np.argmin(final_dists, axis=1)
        inertia = float(np.sum(np.min(final_dists, axis=1) ** 2))

        if inertia < min_inertia:
            min_inertia = inertia
            best_res = {"labels": labels, "centers": centers.copy(), "inertia": inertia, "n_iter": n_iter}

    return best_res


def _memberships(d_sq, m):
    """u_ij = 1 / sum_l (d_ij / d_il)^(2/(m-1)); d_sq - квадраты расстояний [n, c].
    Для точки, совпавшей с центром (d = 0), принадлежность 1 этому центру, остальные 0."""
    n, c = d_sq.shape
    U = np.zeros((n, c))
    zero = d_sq <= 1e-24
    has_zero = zero.any(axis=1)

    # обычные строки: (d_ij/d_il)^(2/(m-1)) = (d_ij^2 / d_il^2)^(1/(m-1))
    regular = ~has_zero
    if regular.any():
        p = 1.0 / (m - 1.0)
        ratio = (d_sq[regular][:, :, None] / d_sq[regular][:, None, :]) ** p   # [n, c, c]
        U[regular] = 1.0 / ratio.sum(axis=2)

    # строки с d = 0: вся принадлежность делится поровну между совпавшими центрами
    if has_zero.any():
        z = zero[has_zero].astype(float)
        U[has_zero] = z / z.sum(axis=1, keepdims=True)
    return U


def cmeans(X, c, measure, m=2.0, n_init=5, max_iter=150, tol=1e-5, seed=0):
    rng = np.random.default_rng(seed)
    best_res = None
    min_cost = float('inf')

    for init_run in range(n_init):
        # Начальная матрица принадлежностей U (случайная, сумма строк = 1)
        U = rng.dirichlet([1.0] * c, size=X.shape[0])
        n_iter = 0

        for iteration in range(max_iter):
            n_iter = iteration + 1
            # Расчет центров: v_j = sum(u_ij^m * x_i) / sum(u_ij^m)
            um = U ** m
            denom = np.sum(um, axis=0).reshape(-1, 1)
            centers = np.dot(um.T, X) / denom

            # Обновление матрицы принадлежностей по расстояниям выбранной меры
            d_sq = pairwise_distance(X, centers, measure) ** 2
            U_new = _memberships(d_sq, m)

            delta = np.max(np.abs(U_new - U))
            U = U_new
            if delta < tol:
                break

        # Целевая функция J = sum(u_ij^m * d_ij^2) для согласованной пары (U, центры)
        um = U ** m
        centers = np.dot(um.T, X) / np.sum(um, axis=0).reshape(-1, 1)
        final_dists_sq = pairwise_distance(X, centers, measure) ** 2
        cost = float(np.sum(um * final_dists_sq))

        if cost < min_cost:
            min_cost = cost
            best_res = {"u": U, "labels": np.argmax(U, axis=1), "centers": centers, "inertia": cost,
                        "n_iter": n_iter}

    return best_res
