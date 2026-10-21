"""
Методы уменьшения пространства признаков и оценка их результата.

Три метода по варианту задания:
  1. PCA   — метод главных компонент (sklearn.decomposition.PCA), линейная проекция,
             новые признаки = линейные комбинации исходных терминов;
  2. AdDel — отбор признаков (Загоруйко, Кутненко): чередование шагов «добавить n
             лучших признаков» и «удалить m худших», m < n; критерий качества —
             FRiS-компактность классов (здесь классы = кластеры-подпапки датасета);
             новые признаки = подмножество ИСХОДНЫХ терминов;
  3. UMAP  — нелинейное вложение (umap-learn), сохраняет локальную структуру соседей.

Вход везде: X [документы × термины] и C [кластеры × термины] — матрицы из лабы 2.
Метод обучается на документах X, а векторы кластеров C проходят через тот же
обученный преобразователь (PCA/UMAP — transform, AdDel — те же столбцы).
"""

import numpy as np
from scipy import stats
from sklearn.decomposition import PCA
from sklearn.manifold import trustworthiness
from sklearn.metrics import silhouette_score
from sklearn.metrics.pairwise import cosine_distances
from sklearn.model_selection import StratifiedKFold
from sklearn.neighbors import KNeighborsClassifier

RANDOM_STATE = 42


# ----------------------------------------------------------------------------
# 1. PCA
# ----------------------------------------------------------------------------
def reduce_pca(X, C, n_components):
    """-> (Xr, Cr, pca). Главные компоненты ищутся по документам (центрирование по
    среднему документов делает сам sklearn); центроиды кластеров проецируются на них."""
    n = min(n_components, X.shape[0] - 1, X.shape[1])
    pca = PCA(n_components=n, svd_solver="full", random_state=RANDOM_STATE)
    Xr = pca.fit_transform(X)
    Cr = pca.transform(C)
    return Xr, Cr, pca


# ----------------------------------------------------------------------------
# 2. AdDel с критерием FRiS-компактности
# ----------------------------------------------------------------------------
def _fris_compactness(D2, y):
    """Компактность классов по матрице квадратов расстояний до центроидов классов.

    D2 — [..., документы, классы]; y — номер класса каждого документа.
    Для документа x:  r_own   — расстояние до центроида СВОЕГО класса,
                      r_rival — расстояние до ближайшего центроида ЧУЖОГО класса,
                      FRiS(x) = (r_rival − r_own) / (r_rival + r_own)  ∈ [−1; 1].
    Компактность = среднее FRiS по документам (1 — классы собраны и далеки друг от друга,
    0 и ниже — документ ближе к чужому центроиду)."""
    D = np.sqrt(np.clip(D2, 0.0, None))
    n, k = D.shape[-2:]
    own_mask = np.zeros((n, k), dtype=bool)
    own_mask[np.arange(n), y] = True
    own = D[..., own_mask]                                   # [..., n]
    rival = np.where(own_mask, np.inf, D).min(axis=-1)       # [..., n]
    denom = rival + own
    fris = np.divide(rival - own, denom, out=np.zeros_like(denom), where=denom > 0)
    return fris.mean(axis=-1)


def addel(X, y, n_add=2, n_del=1, max_features=30):
    """Алгоритм AdDel: «два шага вперёд — один назад» (n_add=2, n_del=1, n_del < n_add).

    Цикл: добавить n_add признаков (каждый раз — тот, при котором компактность
    подсистемы максимальна), затем удалить n_del признаков (каждый раз — тот, без
    которого компактность максимальна). Остановка: компактность после очередного
    цикла упала по сравнению с предыдущим (точка перегиба функции информативности) —
    тогда возвращается набор предыдущего цикла; либо достигнут max_features.

    -> dict: selected (индексы столбцов X в порядке отбора), curve (по циклам:
    число признаков, компактность), history (каждый шаг add/del)."""
    X = np.asarray(X, dtype=float)
    y = np.asarray(y)
    n, n_feat = X.shape
    k = int(y.max()) + 1
    cent = np.vstack([X[y == c].mean(axis=0) for c in range(k)])           # [классы × признаки]
    # вклад каждого признака в квадрат расстояния «документ → центроид класса»
    contrib = (X.T[:, :, None] - cent.T[:, None, :]) ** 2                  # [признаки, документы, классы]

    selected: list[int] = []
    D2 = np.zeros((n, k))
    history, curve = [], []
    prev_c, prev_selected = -np.inf, []

    while len(selected) < max_features:
        for _ in range(n_add):
            comp = _fris_compactness(D2[None] + contrib, y)                # [признаки]
            comp[selected] = -np.inf
            j = int(np.argmax(comp))
            selected.append(j)
            D2 += contrib[j]
            history.append(("add", j, float(comp[j])))
        for _ in range(n_del):
            if len(selected) <= 1:
                break
            comp = _fris_compactness(D2[None] - contrib[selected], y)      # [выбранные]
            r = int(np.argmax(comp))
            j = selected.pop(r)
            D2 -= contrib[j]
            history.append(("del", j, float(comp[r])))

        c_now = float(_fris_compactness(D2, y))
        curve.append((len(selected), c_now))
        if c_now < prev_c:                                                  # компактность упала
            selected = prev_selected
            break
        prev_c, prev_selected = c_now, list(selected)

    return {"selected": selected, "curve": curve, "history": history}


# ----------------------------------------------------------------------------
# 3. UMAP
# ----------------------------------------------------------------------------
def reduce_umap(X, C, n_components, n_neighbors=10, min_dist=0.1):
    """-> (Xr, Cr). Метрика cosine (как принято для tf-idf векторов); random_state задан
    ради воспроизводимости (при этом umap считает в один поток)."""
    import umap  # pip install umap-learn

    model = umap.UMAP(
        n_components=n_components,
        n_neighbors=min(n_neighbors, X.shape[0] - 1),
        min_dist=min_dist,
        metric="cosine",
        random_state=RANDOM_STATE,
    )
    Xr = model.fit_transform(X)
    Cr = model.transform(C)
    return Xr, Cr


# ----------------------------------------------------------------------------
# Проверка результата (верификация)
# ----------------------------------------------------------------------------
def _upper(D):
    return D[np.triu_indices_from(D, k=1)]


def _unit(M):
    """Строки -> единичной длины (нулевые строки остаются нулевыми)."""
    norm = np.linalg.norm(M, axis=1, keepdims=True)
    return M / np.where(norm > 0, norm, 1.0)


def quality(X, Xr, y, n_splits=5):
    """Показатели того, насколько представление Xr сохраняет структуру исходного X.
    Все расстояния — косинусные (не зависят от масштаба весов нейросети).

    - silhouette    — силуэт по кластерам-подпапкам (−1…1; больше — кластеры разделимее);
    - knn_acc       — точность 3-NN по кластерам при стратифицированной кросс-валидации;
    - trustworthiness — доля «ложных соседей», внесённых проекцией (0…1; 1 — нет искажений);
    - dist_spearman — корреляция Спирмена между попарными расстояниями до и после
                      (1 — геометрия документов сохранена)."""
    y = np.asarray(y)
    n_splits = max(2, min(n_splits, int(np.bincount(y).min())))
    cv = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=RANDOM_STATE)
    knn = KNeighborsClassifier(n_neighbors=3, metric="cosine")
    accs = []
    for tr, te in cv.split(Xr, y):
        accs.append(knn.fit(Xr[tr], y[tr]).score(Xr[te], y[te]))
    d_before, d_after = cosine_distances(X), cosine_distances(Xr)
    return {
        "silhouette": float(silhouette_score(Xr, y, metric="cosine")),
        "knn_acc": float(np.mean(accs)),
        # на единичных векторах евклидово расстояние упорядочивает пары так же, как косинусное
        "trustworthiness": float(trustworthiness(_unit(X), _unit(Xr), n_neighbors=5)),
        "dist_spearman": float(stats.spearmanr(_upper(d_before), _upper(d_after)).statistic),
    }


def addel_nested_knn_acc(X, y, n_splits=5, **addel_kwargs):
    """Честная точность 3-NN для AdDel: отбор признаков УЧИТЫВАЕТ метки кластеров, поэтому
    при отборе на всех документах точность завышена (утечка меток). Здесь AdDel запускается
    заново внутри каждой обучающей выборки, а проверка идёт на документах, которых он не видел."""
    y = np.asarray(y)
    n_splits = max(2, min(n_splits, int(np.bincount(y).min())))
    cv = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=RANDOM_STATE)
    knn = KNeighborsClassifier(n_neighbors=3, metric="cosine")
    accs = []
    for tr, te in cv.split(X, y):
        sel = addel(X[tr], y[tr], **addel_kwargs)["selected"]
        accs.append(knn.fit(X[tr][:, sel], y[tr]).score(X[te][:, sel], y[te]))
    return float(np.mean(accs))
