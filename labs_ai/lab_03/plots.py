"""Графики лабы 3 (matplotlib, бэкенд Agg — окна не открываются, файлы пишутся в PNG)."""

import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

METHOD_TITLES = {"original": "до сокращения", "pca": "PCA", "addel": "AdDel", "umap": "UMAP"}
METHOD_COLORS = {"original": "#7f7f7f", "pca": "#1f77b4", "addel": "#2ca02c", "umap": "#d62728"}

# характеристики из лабы 2, для которых строятся распределения «до/после»
PLOT_CHARACTERISTICS = ["среднее", "станд_отклонение", "асимметрия", "эксцесс", "джини", "энтропия_бит"]


def _prepare(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)


def plot_projection(path, labels, cluster_names, panels, title):
    """panels: список (заголовок, подпись_x, подпись_y, X2 [документы×2], C2 [кластеры×2]).
    Точки — документы (цвет = кластер), звёзды — векторы кластеров."""
    _prepare(path)
    cmap = plt.get_cmap("tab10")
    labels = np.asarray(labels)
    fig, axes = plt.subplots(1, len(panels), figsize=(5.2 * len(panels), 4.8))
    axes = np.atleast_1d(axes)
    for ax, (name, xl, yl, X2, C2) in zip(axes, panels):
        for i, c in enumerate(cluster_names):
            m = labels == c
            ax.scatter(X2[m, 0], X2[m, 1], s=28, color=cmap(i), alpha=0.8, label=c)
            ax.scatter(C2[i, 0], C2[i, 1], s=220, marker="*", color=cmap(i), edgecolor="black", linewidth=1.2)
        ax.set_title(name)
        ax.set_xlabel(xl)
        ax.set_ylabel(yl)
        ax.grid(alpha=0.25)
    axes[0].legend(fontsize=7, loc="best")
    fig.suptitle(title)
    fig.tight_layout()
    fig.savefig(path, dpi=130)
    plt.close(fig)


def plot_distributions(path, stats_by_method, title):
    """stats_by_method: {метод: DataFrame характеристик документов (строка — документ)}.
    По каждой характеристике — боксплоты значений по 50 документам для всех методов."""
    _prepare(path)
    methods = list(stats_by_method)
    cols = PLOT_CHARACTERISTICS
    fig, axes = plt.subplots(2, 3, figsize=(14, 7.5))
    for ax, col in zip(axes.ravel(), cols):
        data = [stats_by_method[m][col].dropna().values for m in methods]
        bp = ax.boxplot(data, patch_artist=True, widths=0.6, showfliers=True,
                        flierprops={"markersize": 3})
        for patch, m in zip(bp["boxes"], methods):
            patch.set_facecolor(METHOD_COLORS[m])
            patch.set_alpha(0.6)
        ax.set_xticks(range(1, len(methods) + 1))
        ax.set_xticklabels([METHOD_TITLES[m] for m in methods], fontsize=8)
        ax.set_title(col)
        ax.grid(alpha=0.25)
    fig.suptitle(title)
    fig.tight_layout()
    fig.savefig(path, dpi=130)
    plt.close(fig)


def plot_component_values(path, matrices, title):
    """Гистограммы значений ВСЕХ компонент всех векторов документов до и после
    (ось Y логарифмическая: у исходных векторов почти все значения — нули)."""
    _prepare(path)
    methods = list(matrices)
    fig, axes = plt.subplots(1, len(methods), figsize=(4.2 * len(methods), 3.8))
    for ax, m in zip(np.atleast_1d(axes), methods):
        ax.hist(matrices[m].ravel(), bins=60, color=METHOD_COLORS[m], alpha=0.8)
        ax.set_yscale("log")
        ax.set_title(f"{METHOD_TITLES[m]} ({matrices[m].shape[1]} признаков)")
        ax.set_xlabel("значение компоненты")
        ax.grid(alpha=0.25)
    fig.suptitle(title)
    fig.tight_layout()
    fig.savefig(path, dpi=130)
    plt.close(fig)


def plot_addel_curve(path, curve, title):
    """Функция информативности AdDel: компактность после каждого цикла."""
    _prepare(path)
    ns, cs = zip(*curve)
    fig, ax = plt.subplots(figsize=(5.5, 3.8))
    ax.plot(ns, cs, marker="o", color=METHOD_COLORS["addel"])
    ax.set_xlabel("число признаков в подсистеме")
    ax.set_ylabel("FRiS-компактность")
    ax.set_title(title)
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(path, dpi=130)
    plt.close(fig)


def plot_pca_variance(path, ratios, title):
    _prepare(path)
    fig, ax = plt.subplots(figsize=(5.5, 3.8))
    x = np.arange(1, len(ratios) + 1)
    ax.bar(x, ratios, color=METHOD_COLORS["pca"], alpha=0.7, label="доля дисперсии компоненты")
    ax.plot(x, np.cumsum(ratios), color="black", marker="o", label="накопленная доля")
    ax.set_xlabel("номер главной компоненты")
    ax.set_title(title)
    ax.legend()
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(path, dpi=130)
    plt.close(fig)


QUALITY_METRICS = [("silhouette", "силуэт по кластерам"),
                   ("knn_acc_без_утечки", "точность 3-NN (AdDel — без утечки меток)"),
                   ("trustworthiness", "trustworthiness"),
                   ("dist_spearman", "корреляция попарных расстояний")]


def _grouped_bars(ax, df, value, ais, methods):
    """df: строки (нейросеть, метод) -> value. Группа столбиков = нейросеть, цвет = метод."""
    w = 0.8 / len(methods)
    for k, m in enumerate(methods):
        vals = [df[(df["нейросеть"] == a) & (df["метод"] == m)][value].mean() for a in ais]
        ax.bar(np.arange(len(ais)) + (k - (len(methods) - 1) / 2) * w, vals, w,
               color=METHOD_COLORS[m], label=METHOD_TITLES[m], alpha=0.85)
    ax.set_xticks(np.arange(len(ais)))
    ax.set_xticklabels(ais, fontsize=8)
    ax.grid(axis="y", alpha=0.25)


def plot_comparison_quality(path, df, ais, vector_types):
    """Сравнение нейросетей и методов по показателям сохранения структуры.
    Строка — тип векторов, столбец — показатель."""
    _prepare(path)
    methods = ["original", "pca", "addel", "umap"]
    fig, axes = plt.subplots(len(vector_types), len(QUALITY_METRICS),
                             figsize=(4.4 * len(QUALITY_METRICS), 3.6 * len(vector_types)), squeeze=False)
    for r, vt in enumerate(vector_types):
        sub = df[df["тип_векторов"] == vt]
        for c, (col, title) in enumerate(QUALITY_METRICS):
            ax = axes[r][c]
            _grouped_bars(ax, sub, col, ais, methods)
            ax.set_title(f"{title}\n{vt}", fontsize=9)
            ax.set_ylim(0, 1.05)
    axes[0][0].legend(fontsize=8)
    fig.suptitle("Сравнение нейросетей и методов уменьшения признаков")
    fig.tight_layout()
    fig.savefig(path, dpi=130)
    plt.close(fig)


def plot_comparison_characteristics(path, df, ais, vector_types):
    """Средние по документам значения характеристик до/после для каждой нейросети."""
    _prepare(path)
    methods = ["original", "pca", "addel", "umap"]
    fig, axes = plt.subplots(len(vector_types), len(PLOT_CHARACTERISTICS),
                             figsize=(3.6 * len(PLOT_CHARACTERISTICS), 3.4 * len(vector_types)), squeeze=False)
    for r, vt in enumerate(vector_types):
        sub = df[df["тип_векторов"] == vt]
        for c, col in enumerate(PLOT_CHARACTERISTICS):
            ax = axes[r][c]
            _grouped_bars(ax, sub, col, ais, methods)
            ax.set_title(f"{col}\n{vt}", fontsize=9)
    axes[0][0].legend(fontsize=7)
    fig.suptitle("Средние по документам значения характеристик до и после уменьшения признаков")
    fig.tight_layout()
    fig.savefig(path, dpi=130)
    plt.close(fig)
