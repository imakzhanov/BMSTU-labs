"""Графики лабы 5 (matplotlib, бэкенд Agg)."""

import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

CLF_COLORS = {"logreg": "#1f77b4", "knn": "#2ca02c", "tree": "#d62728"}


def _prepare(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)


def plot_confusions(path, confusions, classes, title):
    """confusions: {классификатор: матрица ошибок}. Строка — истинный класс, столбец — предсказанный."""
    _prepare(path)
    fig, axes = plt.subplots(1, len(confusions), figsize=(5.6 * len(confusions), 5.2), squeeze=False)
    for ax, (name, cm) in zip(axes[0], confusions.items()):
        ax.imshow(cm, cmap="Blues")
        ax.set_xticks(range(len(classes)))
        ax.set_yticks(range(len(classes)))
        ax.set_xticklabels(classes, rotation=45, ha="right", fontsize=7)
        ax.set_yticklabels(classes, fontsize=7)
        thr = cm.max() / 2 if cm.max() else 1
        for i in range(cm.shape[0]):
            for j in range(cm.shape[1]):
                ax.text(j, i, int(cm[i, j]), ha="center", va="center", fontsize=8,
                        color="white" if cm[i, j] > thr else "black")
        ax.set_xlabel("предсказано")
        ax.set_ylabel("истинный класс")
        ax.set_title(name, fontsize=10)
    fig.suptitle(title)
    fig.tight_layout()
    fig.savefig(path, dpi=130)
    plt.close(fig)


def plot_heatmap(path, table, title, ylabel_note=""):
    """table: DataFrame (строки — наборы признаков, столбцы — классификаторы), значения 0…1."""
    _prepare(path)
    fig, ax = plt.subplots(figsize=(1.8 * table.shape[1] + 3, 0.5 * table.shape[0] + 1.8))
    im = ax.imshow(table.values.astype(float), cmap="YlGn", vmin=0, vmax=1, aspect="auto")
    ax.set_xticks(range(table.shape[1]))
    ax.set_xticklabels(table.columns, fontsize=9)
    ax.set_yticks(range(table.shape[0]))
    ax.set_yticklabels(table.index, fontsize=9)
    for i in range(table.shape[0]):
        for j in range(table.shape[1]):
            v = table.values[i, j]
            if v == v:
                ax.text(j, i, f"{v:.2f}", ha="center", va="center", fontsize=9)
    fig.colorbar(im, ax=ax, fraction=0.04)
    ax.set_title(title)
    fig.tight_layout()
    fig.savefig(path, dpi=130)
    plt.close(fig)


def plot_bars(path, tables, titles, suptitle):
    """tables: список DataFrame (наборы × классификаторы) — по одному на панель."""
    _prepare(path)
    fig, axes = plt.subplots(len(tables), 1, figsize=(11, 3.8 * len(tables)), squeeze=False)
    for ax, tbl, title in zip(axes[:, 0], tables, titles):
        n = tbl.shape[1]
        w = 0.8 / n
        for k, clf in enumerate(tbl.columns):
            ax.bar(np.arange(len(tbl)) + (k - (n - 1) / 2) * w, tbl[clf].values, w,
                   label=clf, color=CLF_COLORS.get(clf), alpha=0.85)
        ax.set_xticks(range(len(tbl)))
        ax.set_xticklabels(tbl.index, rotation=25, ha="right", fontsize=8)
        ax.set_ylim(0, 1.05)
        ax.set_title(title, fontsize=10)
        ax.grid(axis="y", alpha=0.25)
    axes[0][0].legend(fontsize=8, ncol=3)
    fig.suptitle(suptitle)
    fig.tight_layout()
    fig.savefig(path, dpi=130)
    plt.close(fig)
