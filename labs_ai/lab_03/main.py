"""
Лабораторная 3: уменьшение пространства признаков векторов документов и кластеров.

Исходные векторы — те же, что в лабе 2 (labs_ai/lab_02: загрузка выхлопа лабы 1 всех
четырёх нейросетей, центроиды кластеров, 18 статистических характеристик). Модули
vectors.py и characteristics.py берутся из lab_02 без копирования.

Для каждой из 4 нейросетей и каждого из 2 типов векторов (doc_wordforms / doc_lemmas):
  1. загружаются векторы 50 документов и строятся векторы 7 кластеров (лаба 2);
  2. применяются три метода из reduction.py:  PCA, AdDel, UMAP
     (метод обучается на документах, центроиды кластеров проходят через него же);
  3. для векторов до и после считаются 18 характеристик (characteristics.describe);
  4. считаются показатели сохранения структуры (силуэт, точность 3-NN, trustworthiness,
     корреляция попарных расстояний);
  5. сохраняются CSV и графики (распределения характеристик до/после, проекции на
     плоскость, кривая AdDel, дисперсия PCA).

Результаты: output/<нейросеть>/<тип_векторов>/…, output/comparison_reduction.csv,
            output/comparison_characteristics.csv и графики сравнения output/comparison_*.png.

Запуск:  pip install scikit-learn umap-learn matplotlib   (один раз)
         python main.py
"""

import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "lab_02"))   # vectors.py, characteristics.py из лабы 2

from vectors import AI_NAMES, VECTOR_TYPES, load_doc_vectors, build_cluster_vectors, cluster_of  # noqa: E402
from characteristics import describe, gini, shannon_entropy  # noqa: E402

import plots  # noqa: E402
import reduction  # noqa: E402

OUT = os.path.join(HERE, "output")

N_COMPONENTS = 10      # размерность после PCA и UMAP
ADDEL_N_ADD = 2        # AdDel: за цикл добавляется 2 признака...
ADDEL_N_DEL = 1        # ...и удаляется 1 («два шага вперёд — один назад»)
ADDEL_MAX = 30         # верхняя граница числа признаков AdDel


def save(df: pd.DataFrame, path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, sep=";", decimal=",", encoding="utf-8-sig", float_format="%.6g")


def describe_vector(x) -> dict:
    """Те же 18 характеристик, что в лабе 2. После PCA/UMAP значения компонент бывают
    отрицательными, а коэффициент Джини и энтропия Шеннона определены только для
    неотрицательных значений — для них берётся модуль |x| (для исходных векторов он
    ничего не меняет). Остальные характеристики считаются по значениям как есть."""
    x = np.asarray(x, dtype=float)
    with np.errstate(all="ignore"):          # describe() считает энтропию и по отрицательным x -> NaN, ниже значение заменяется
        res = describe(x)
    res["джини"] = gini(np.abs(x))
    res["энтропия_бит"] = shannon_entropy(np.abs(x))
    return res


def stats_table(names, M) -> pd.DataFrame:
    return pd.DataFrame.from_dict({n: describe_vector(v) for n, v in zip(names, M)}, orient="index")


def process(ai_name: str, vector_type: str):
    """-> (строки показателей качества, строки средних характеристик) для сводных таблиц и графиков."""
    out_dir = os.path.join(OUT, ai_name, vector_type)
    tag = f"{ai_name} / {vector_type}"

    doc_names, features, X = load_doc_vectors(ai_name, vector_type)
    cluster_names, C = build_cluster_vectors(doc_names, X)
    labels = [cluster_of(n) for n in doc_names]
    y = np.array([cluster_names.index(c) for c in labels])
    features = np.asarray(features)

    # ---- 1. PCA ----
    X_pca, C_pca, pca = reduction.reduce_pca(X, C, N_COMPONENTS)
    pc_names = [f"PC{i + 1}" for i in range(X_pca.shape[1])]
    save(pd.DataFrame(X_pca, index=doc_names, columns=pc_names), os.path.join(out_dir, "pca_docs.csv"))
    save(pd.DataFrame(C_pca, index=cluster_names, columns=pc_names), os.path.join(out_dir, "pca_clusters.csv"))
    save(pd.DataFrame({"доля_дисперсии": pca.explained_variance_ratio_,
                       "накопленная": np.cumsum(pca.explained_variance_ratio_)}, index=pc_names),
         os.path.join(out_dir, "pca_explained_variance.csv"))
    # интерпретация: термины с наибольшими по модулю нагрузками каждой компоненты
    top_rows = {}
    for i, comp in enumerate(pca.components_):
        order = np.argsort(comp)
        plus = [f"{features[j]} ({comp[j]:+.3f})" for j in order[::-1][:8]]
        minus = [f"{features[j]} ({comp[j]:+.3f})" for j in order[:8]]
        top_rows[pc_names[i]] = {"положительные_нагрузки": ", ".join(plus), "отрицательные_нагрузки": ", ".join(minus)}
    save(pd.DataFrame.from_dict(top_rows, orient="index"), os.path.join(out_dir, "pca_top_terms.csv"))

    # ---- 2. AdDel ----
    res = reduction.addel(X, y, n_add=ADDEL_N_ADD, n_del=ADDEL_N_DEL, max_features=ADDEL_MAX)
    sel = res["selected"]
    sel_names = [str(features[j]) for j in sel]
    X_ad, C_ad = X[:, sel], C[:, sel]
    save(pd.DataFrame(X_ad, index=doc_names, columns=sel_names), os.path.join(out_dir, "addel_docs.csv"))
    save(pd.DataFrame(C_ad, index=cluster_names, columns=sel_names), os.path.join(out_dir, "addel_clusters.csv"))
    # какие термины отобраны и в каких кластерах они «живут» (средний вес по кластеру)
    sel_table = pd.DataFrame(C_ad.T, index=sel_names, columns=cluster_names)
    sel_table.insert(0, "порядок_отбора", range(1, len(sel) + 1))
    save(sel_table, os.path.join(out_dir, "addel_selected_features.csv"))
    save(pd.DataFrame(res["curve"], columns=["признаков", "компактность"]), os.path.join(out_dir, "addel_curve.csv"))
    save(pd.DataFrame([(a, str(features[j]), c) for a, j, c in res["history"]],
                      columns=["шаг", "признак", "компактность_после_шага"]),
         os.path.join(out_dir, "addel_history.csv"))

    # ---- 3. UMAP ----
    X_um, C_um = reduction.reduce_umap(X, C, N_COMPONENTS)
    um_names = [f"UMAP{i + 1}" for i in range(X_um.shape[1])]
    save(pd.DataFrame(X_um, index=doc_names, columns=um_names), os.path.join(out_dir, "umap_docs.csv"))
    save(pd.DataFrame(C_um, index=cluster_names, columns=um_names), os.path.join(out_dir, "umap_clusters.csv"))

    # ---- характеристики до / после ----
    docs = {"original": X, "pca": X_pca, "addel": X_ad, "umap": X_um}
    clus = {"original": C, "pca": C_pca, "addel": C_ad, "umap": C_um}
    stats_docs = {m: stats_table(doc_names, M) for m, M in docs.items()}
    for m, df in stats_docs.items():
        save(df, os.path.join(out_dir, f"stats_docs_{m}.csv"))
        save(stats_table(cluster_names, clus[m]), os.path.join(out_dir, f"stats_clusters_{m}.csv"))
    char_summary = pd.DataFrame({m: df.mean() for m, df in stats_docs.items()}).T
    save(char_summary, os.path.join(out_dir, "characteristics_summary.csv"))
    char_rows = [{"нейросеть": ai_name, "тип_векторов": vector_type, "метод": m, **row.to_dict()}
                 for m, row in char_summary.iterrows()]

    # ---- показатели сохранения структуры ----
    ad_nested = reduction.addel_nested_knn_acc(X, y, n_add=ADDEL_N_ADD, n_del=ADDEL_N_DEL, max_features=ADDEL_MAX)
    rows = []
    for m, M in docs.items():
        q = reduction.quality(X, M, y)
        q["knn_acc_без_утечки"] = ad_nested if m == "addel" else q["knn_acc"]
        q["доля_дисперсии"] = float(pca.explained_variance_ratio_.sum()) if m == "pca" else np.nan
        rows.append({"нейросеть": ai_name, "тип_векторов": vector_type, "метод": m,
                     "признаков": M.shape[1], **q})
    save(pd.DataFrame(rows).set_index(["метод"]).drop(columns=["нейросеть", "тип_векторов"]),
         os.path.join(out_dir, "quality.csv"))

    # ---- графики ----
    X_um2, C_um2 = reduction.reduce_umap(X, C, 2)
    plots.plot_projection(
        os.path.join(out_dir, "projection.png"), labels, cluster_names,
        [("PCA", "PC1", "PC2", X_pca[:, :2], C_pca[:, :2]),
         ("AdDel (первые два отобранных признака)", sel_names[0], sel_names[min(1, len(sel) - 1)],
          X_ad[:, :2] if len(sel) > 1 else np.c_[X_ad, X_ad], C_ad[:, :2] if len(sel) > 1 else np.c_[C_ad, C_ad]),
         ("UMAP (отдельное вложение в 2D)", "UMAP1", "UMAP2", X_um2, C_um2)],
        f"{tag}: документы (точки) и кластеры (звёзды)")
    plots.plot_distributions(os.path.join(out_dir, "distributions.png"), stats_docs,
                             f"{tag}: распределение характеристик векторов документов до и после")
    plots.plot_component_values(os.path.join(out_dir, "component_values.png"), docs,
                                f"{tag}: значения компонент векторов документов")
    plots.plot_addel_curve(os.path.join(out_dir, "addel_curve.png"), res["curve"], f"{tag}: AdDel")
    plots.plot_pca_variance(os.path.join(out_dir, "pca_variance.png"), pca.explained_variance_ratio_, f"{tag}: PCA")
    return rows, char_rows


def main() -> None:
    os.makedirs(OUT, exist_ok=True)
    all_rows, all_chars = [], []
    for ai_name in AI_NAMES:
        for vector_type in VECTOR_TYPES:
            print(f"{ai_name} / {vector_type} ...", flush=True)
            rows, char_rows = process(ai_name, vector_type)
            all_rows += rows
            all_chars += char_rows

    quality_df, chars_df = pd.DataFrame(all_rows), pd.DataFrame(all_chars)
    comparison = quality_df.set_index(["нейросеть", "тип_векторов", "метод"])
    save(comparison, os.path.join(OUT, "comparison_reduction.csv"))
    save(chars_df.set_index(["нейросеть", "тип_векторов", "метод"]), os.path.join(OUT, "comparison_characteristics.csv"))

    # сводные графики сравнения нейросетей и методов
    plots.plot_comparison_quality(os.path.join(OUT, "comparison_quality.png"), quality_df, AI_NAMES, VECTOR_TYPES)
    plots.plot_comparison_characteristics(os.path.join(OUT, "comparison_characteristics.png"),
                                          chars_df, AI_NAMES, VECTOR_TYPES)
    print("\nСохранение структуры после уменьшения признаков:")
    print(comparison.round(3).to_string())


if __name__ == "__main__":
    main()
