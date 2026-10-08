"""
Лабораторная 2: векторы документов и кластеров и их статистические характеристики,
построенные ПО ВЫХЛОПУ ЛАБЫ 1 — по векторам, которые для каждого документа уже
посчитали 4 нейросети (deepseek, qwen, gigachat, korolev-ai) в двух вариантах
векторизации (doc_wordforms — по словоформам, doc_lemmas — по леммам pymorphy3).

Для каждой из 4 нейросетей и каждого из 2 вариантов (8 комбинаций всего):
  1. vectors.load_doc_vectors()      -> векторы 50 документов
                                         (из labs_ai/lab_01/<нейросеть>/output/*.json)
  2. vectors.build_cluster_vectors() -> векторы 7 кластеров (центроиды; кластеры
                                         уже заданы — это подпапки «тексты»)
  3. characteristics.describe()      -> 18 характеристик каждого вектора
                                         (по всем компонентам и отдельно по ненулевым)
  4. characteristics.correlations()  -> корреляции Пирсона и Спирмена между векторами,
     characteristics.pair_correlation() -> корреляция документа со своим кластером

Результаты — в output/<нейросеть>/<тип_векторов>/*.csv (11 файлов на комбинацию,
разделитель «;», открываются в Excel) и итоговая сравнительная таблица
output/comparison_summary.csv (сравнение всех 4 нейросетей между собой).

Запуск: python main.py
"""

import os

import numpy as np
import pandas as pd

from vectors import AI_NAMES, VECTOR_TYPES, load_doc_vectors, build_cluster_vectors, cluster_of
from characteristics import describe, correlations, pair_correlation

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")


def save(df: pd.DataFrame, path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, sep=";", decimal=",", encoding="utf-8-sig", float_format="%.6g")


def stats_table(names, M, nonzero_only: bool) -> pd.DataFrame:
    rows = {name: describe(v[v > 0] if nonzero_only else v) for name, v in zip(names, M)}
    return pd.DataFrame.from_dict(rows, orient="index")


def process(ai_name: str, vector_type: str) -> dict:
    """Полный расчёт для одной нейросети и одного типа векторов.
    Сохраняет 11 CSV в output/<ai_name>/<vector_type>/ и возвращает сводную строку
    для итоговой сравнительной таблицы."""
    out_dir = os.path.join(OUT, ai_name, vector_type)

    doc_names, features, X = load_doc_vectors(ai_name, vector_type)
    cluster_names, C = build_cluster_vectors(doc_names, X)

    save(pd.DataFrame(X, index=doc_names, columns=features), os.path.join(out_dir, "doc_vectors.csv"))
    save(pd.DataFrame(C, index=cluster_names, columns=features), os.path.join(out_dir, "cluster_vectors.csv"))

    # характеристики: строка - вектор, столбцы - характеристики
    docs_all = stats_table(doc_names, X, nonzero_only=False)
    docs_nz = stats_table(doc_names, X, nonzero_only=True)

    ci = {c: i for i, c in enumerate(cluster_names)}
    pairs = [pair_correlation(X[i], C[ci[cluster_of(n)]]) for i, n in enumerate(doc_names)]
    docs_all.insert(0, "кластер", [cluster_of(n) for n in doc_names])
    docs_all["пирсон_с_кластером"] = [p for p, _ in pairs]
    docs_all["спирмен_с_кластером"] = [s for _, s in pairs]

    save(docs_all, os.path.join(out_dir, "stats_docs.csv"))
    save(docs_nz, os.path.join(out_dir, "stats_docs_nonzero.csv"))
    save(stats_table(cluster_names, C, nonzero_only=False), os.path.join(out_dir, "stats_clusters.csv"))
    save(stats_table(cluster_names, C, nonzero_only=True), os.path.join(out_dir, "stats_clusters_nonzero.csv"))

    # корреляции между векторами
    for label, names, M in (("docs", doc_names, X), ("clusters", cluster_names, C)):
        pearson, spearman = correlations(M)
        save(pd.DataFrame(pearson, index=names, columns=names), os.path.join(out_dir, f"pearson_{label}.csv"))
        save(pd.DataFrame(spearman, index=names, columns=names), os.path.join(out_dir, f"spearman_{label}.csv"))

    # сводка: среднее каждой характеристики по документам каждого кластера
    summary = docs_all.groupby("кластер").mean(numeric_only=True)
    save(summary, os.path.join(out_dir, "summary_by_cluster.csv"))

    return {
        "нейросеть": ai_name,
        "тип_векторов": vector_type,
        "признаков": X.shape[1],
        "плотность_ср": float(np.count_nonzero(X) / X.size),
        "энтропия_ср": float(docs_nz["энтропия_бит"].mean()),
        "джини_ср": float(docs_nz["джини"].mean()),
        "пирсон_с_кластером_ср": float(docs_all["пирсон_с_кластером"].mean()),
        "спирмен_с_кластером_ср": float(docs_all["спирмен_с_кластером"].mean()),
    }


def main() -> None:
    os.makedirs(OUT, exist_ok=True)
    summary_rows = []
    for ai_name in AI_NAMES:
        for vector_type in VECTOR_TYPES:
            print(f"{ai_name} / {vector_type} ...")
            summary_rows.append(process(ai_name, vector_type))

    comparison = pd.DataFrame(summary_rows).set_index(["нейросеть", "тип_векторов"])
    save(comparison, os.path.join(OUT, "comparison_summary.csv"))

    print("\nСравнение нейросетей (средние по документам, только ненулевые компоненты):")
    print(comparison.round(4).to_string())


if __name__ == "__main__":
    main()
