"""Графики кластеризации (matplotlib, бэкенд Agg: окна не открываются, файлы пишутся в PNG)."""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn.decomposition import PCA

from distances import MEASURES

ALGS = [("kmeans", "k-средних"), ("cmeans", "c-средних")]
MARKERS = ["o", "s", "^", "v", "D", "P", "X", "*"]      # форма точки = настоящая тема


def _combos():
    return [(a, an, m) for a, an in ALGS for m in MEASURES]


def plot_clusters_pca(path, X, true_labels, themes, found, centers, k_opts, metrics, title):
    """Документы на плоскости двух главных компонент (PCA нужна только для рисунка, кластеризация
    шла в полном пространстве). Цвет = найденный кластер, форма = настоящая тема, звезда = центр.
    Строка — алгоритм, столбец — мера; в заголовке k и ARI."""
    pca = PCA(n_components=2, svd_solver="full").fit(X)
    P = pca.transform(X)
    cmap = plt.get_cmap("tab20")
    fig, axes = plt.subplots(2, 3, figsize=(16, 9.5), squeeze=False)
    for ax, (alg, alg_name, measure) in zip(axes.ravel(), _combos()):
        col = f"{alg}_{measure}"
        lab = np.asarray(found[col])
        for t, theme in enumerate(themes):
            m = true_labels == t
            ax.scatter(P[m, 0], P[m, 1], c=[cmap(int(l) % 20) for l in lab[m]], marker=MARKERS[t % len(MARKERS)],
                       s=55, edgecolor="black", linewidth=0.5, alpha=0.9, label=theme)
        C = pca.transform(centers[col])
        ax.scatter(C[:, 0], C[:, 1], c=[cmap(j % 20) for j in range(len(C))], marker="*", s=330,
                   edgecolor="black", linewidth=1.3, zorder=5)
        ax.set_title(f"{alg_name}, {measure} ({MEASURES[measure]})\nk={k_opts[col]}, ARI={metrics[col]['ARI']:.2f}",
                     fontsize=10)
        ax.set_xlabel("PC1")
        ax.set_ylabel("PC2")
        ax.grid(alpha=0.25)
    handles, labels_ = axes[0][0].get_legend_handles_labels()
    for h in handles:
        h.set_facecolor("lightgray")
    fig.legend(handles, labels_, loc="lower center", ncol=len(themes), fontsize=8, title="форма точки = настоящая тема")
    fig.suptitle(f"{title}\nцвет = найденный кластер, звезда = его центр", fontsize=12)
    fig.tight_layout(rect=(0, 0.06, 1, 0.95))
    fig.savefig(path, dpi=130)
    plt.close(fig)


def plot_contingency(path, true_labels, themes, found, k_opts, title):
    """Таблицы сопряжённости: строка — найденный кластер, столбец — настоящая тема, в клетке число
    документов. Хорошая кластеризация — по одной яркой клетке в каждой строке."""
    fig, axes = plt.subplots(2, 3, figsize=(17, 9.5), squeeze=False)
    short = [t if len(t) <= 14 else t[:13] + "…" for t in themes]
    for ax, (alg, alg_name, measure) in zip(axes.ravel(), _combos()):
        col = f"{alg}_{measure}"
        lab = np.asarray(found[col])
        clusters = sorted(set(lab.tolist()))
        M = np.array([[np.sum((lab == c) & (true_labels == t)) for t in range(len(themes))] for c in clusters])
        # строки сортируем по основной теме, чтобы диагональ была видна
        M = M[np.lexsort((-M.max(axis=1), M.argmax(axis=1)))]
        im = ax.imshow(M, cmap="Blues", aspect="auto", vmin=0)
        for i in range(M.shape[0]):
            for j in range(M.shape[1]):
                if M[i, j]:
                    ax.text(j, i, int(M[i, j]), ha="center", va="center", fontsize=8,
                            color="white" if M[i, j] > M.max() / 2 else "black")
        ax.set_xticks(range(len(themes)))
        ax.set_xticklabels(short, rotation=40, ha="right", fontsize=7)
        ax.set_yticks(range(M.shape[0]))
        ax.set_yticklabels([f"кластер {i + 1}" for i in range(M.shape[0])], fontsize=7)
        ax.set_title(f"{alg_name}, {measure} (k={k_opts[col]})", fontsize=10)
    fig.suptitle(f"{title}\nсостав найденных кластеров по настоящим темам (число документов)", fontsize=12)
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    fig.savefig(path, dpi=130)
    plt.close(fig)


def plot_memberships(path, true_labels, themes, doc_names, memberships, k_opts, title):
    """Матрицы принадлежностей c-средних: строка — документ (отсортированы по настоящей теме,
    белые линии — границы тем), столбец — кластер. Если цвет по строке почти ровный —
    алгоритм не уверен, к какому кластеру относится документ."""
    order = np.argsort(true_labels, kind="stable")
    bounds = np.where(np.diff(true_labels[order]) != 0)[0] + 0.5
    fig, axes = plt.subplots(1, 3, figsize=(15, 8), squeeze=False)
    for ax, measure in zip(axes[0], MEASURES):
        U = memberships[measure][order]
        im = ax.imshow(U, cmap="viridis", aspect="auto", vmin=0, vmax=1)   # единая шкала 0-1: ровный тёмный цвет = алгоритм не уверен
        for b in bounds:
            ax.axhline(b, color="white", linewidth=1.2)
        mid = [(np.where(true_labels[order] == t)[0].mean()) for t in range(len(themes))]
        ax.set_yticks(mid)
        ax.set_yticklabels(themes, fontsize=7)
        ax.set_xticks(range(U.shape[1]))
        ax.set_xticklabels([str(j + 1) for j in range(U.shape[1])], fontsize=8)
        ax.set_xlabel("кластер")
        ax.set_title(f"{measure} ({MEASURES[measure]}), k={k_opts[f'cmeans_{measure}']}\n"
                     f"средняя макс. принадлежность {memberships[measure].max(axis=1).mean():.2f}", fontsize=10)
        fig.colorbar(im, ax=ax, fraction=0.046, pad=0.03)
    fig.suptitle(f"{title}\nпринадлежность документов кластерам, c-средних", fontsize=12)
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    fig.savefig(path, dpi=130)
    plt.close(fig)


def plot_summary_heatmaps(path, summary_df):
    """Сводные тепловые карты по всем 8 наборам и 6 комбинациям алгоритм/мера:
    ARI (совпадение с настоящими темами), силуэт и выбранное методом локтя k."""
    df = summary_df.copy()
    df["набор"] = df["нейросеть"] + " / " + df["тип_векторов"].str.replace("doc_", "")
    df["комбинация"] = df["алгоритм"] + "\n" + df["мера"]
    cols = [f"{a}\n{m}" for a, _, m in _combos()]
    rows = list(dict.fromkeys(df["набор"]))
    fig, axes = plt.subplots(1, 3, figsize=(19, 6.5))
    for ax, (value, title, cmap, vmin, vmax) in zip(
            axes, [("ARI", "ARI при k из метода локтя", "YlGn", 0, 1),
                   ("silhouette", "силуэт при k из метода локтя", "PuBu", None, None),
                   ("k_opt", "оптимальное k (метод локтя)", "Oranges", 2, 15)]):
        piv = df.pivot(index="набор", columns="комбинация", values=value).loc[rows, cols]
        im = ax.imshow(piv.values, cmap=cmap, aspect="auto", vmin=vmin, vmax=vmax)
        for i in range(piv.shape[0]):
            for j in range(piv.shape[1]):
                v = piv.values[i, j]
                ax.text(j, i, f"{v:.0f}" if value == "k_opt" else f"{v:.2f}", ha="center", va="center", fontsize=8)
        ax.set_xticks(range(len(cols)))
        ax.set_xticklabels(cols, fontsize=8)
        ax.set_yticks(range(len(rows)))
        ax.set_yticklabels(rows, fontsize=8)
        ax.set_title(title)
        fig.colorbar(im, ax=ax, fraction=0.046, pad=0.03)
    fig.suptitle("Сравнение кластеризаций: наборы векторов × алгоритм × мера близости", fontsize=13)
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fig.savefig(path, dpi=130)
    plt.close(fig)


def plot_proximity_mds(path, X, true_labels, themes, found, centers, k_opts, metrics, title):
    """Мера близости «на плоскости x-y»: документы и центры кластеров размещаются на плоскости так,
    чтобы расстояния между точками как можно точнее повторяли расстояния ВЫБРАННОЙ меры
    (многомерное шкалирование MDS по матрице расстояний euclid / tanimoto / pearson).
    Чем ближе точки на рисунке, тем они ближе по мере. Цвет = найденный кластер, форма = настоящая
    тема, звезда = центр кластера. В заголовке stress-1: доля искажения расстояний (0 — идеально,
    до ~0,2 — рисунку можно доверять)."""
    import warnings
    from scipy.spatial.distance import pdist
    from sklearn.manifold import MDS
    from distances import pairwise_distance

    cmap = plt.get_cmap("tab20")
    fig, axes = plt.subplots(2, 3, figsize=(16, 9.5), squeeze=False)
    n = X.shape[0]
    for ax, (alg, alg_name, measure) in zip(axes.ravel(), _combos()):
        col = f"{alg}_{measure}"
        lab = np.asarray(found[col])
        Z = np.vstack([X, centers[col]])                      # документы + центры кластеров
        D = pairwise_distance(Z, Z, measure)
        D = (D + D.T) / 2.0
        np.fill_diagonal(D, 0.0)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", FutureWarning)   # смена параметров MDS в новых версиях sklearn
            E = MDS(n_components=2, dissimilarity="precomputed", random_state=0, n_init=4, max_iter=500).fit_transform(D)
        d_true = D[np.triu_indices_from(D, k=1)]
        stress1 = float(np.sqrt(np.sum((d_true - pdist(E)) ** 2) / np.sum(d_true ** 2)))

        for t, theme in enumerate(themes):
            m = true_labels == t
            ax.scatter(E[:n][m, 0], E[:n][m, 1], c=[cmap(int(l) % 20) for l in lab[m]],
                       marker=MARKERS[t % len(MARKERS)], s=55, edgecolor="black", linewidth=0.5, alpha=0.9, label=theme)
        ax.scatter(E[n:, 0], E[n:, 1], c=[cmap(j % 20) for j in range(len(E) - n)], marker="*", s=330,
                   edgecolor="black", linewidth=1.3, zorder=5)
        ax.set_title(f"{alg_name}, {measure} ({MEASURES[measure]})\nk={k_opts[col]}, ARI={metrics[col]['ARI']:.2f}, "
                     f"stress-1={stress1:.2f}", fontsize=10)
        ax.set_xlabel("x (MDS 1)")
        ax.set_ylabel("y (MDS 2)")
        ax.set_aspect("equal", adjustable="datalim")
        ax.grid(alpha=0.25)
    handles, labels_ = axes[0][0].get_legend_handles_labels()
    for h in handles:
        h.set_facecolor("lightgray")
    fig.legend(handles, labels_, loc="lower center", ncol=len(themes), fontsize=8, title="форма точки = настоящая тема")
    fig.suptitle(f"{title}\nрасстояние между точками на плоскости = расстояние по выбранной мере близости", fontsize=12)
    fig.tight_layout(rect=(0, 0.06, 1, 0.94))
    fig.savefig(path, dpi=130)
    plt.close(fig)
