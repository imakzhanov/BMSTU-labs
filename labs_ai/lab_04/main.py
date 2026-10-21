import os, sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")                      # без окон, графики пишутся в файлы
import matplotlib.pyplot as plt

# Подключение модуля vectors.py из lab_02
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "lab_02"))
from vectors import AI_NAMES, VECTOR_TYPES, load_doc_vectors, cluster_of

from distances import MEASURES
from clustering import kmeans, cmeans
from evaluation import elbow_point, external_metrics, silhouette
import plots

OUT = os.path.join(HERE, "output")         # результаты не зависят от текущей папки запуска
KS = list(range(2, 16))                    # проверяемые числа кластеров
K_TRUE = 7                                 # настоящее число тем


def save_csv(df, path, index=False):
    df.to_csv(path, sep=";", decimal=",", encoding="utf-8-sig", float_format="%.6g", index=index)


def run_experiment():
    summary_data = []

    for ai_name in AI_NAMES:
        for vec_type in VECTOR_TYPES:
            print(f"Processing {ai_name} | {vec_type}...", flush=True)
            doc_names, features, X = load_doc_vectors(ai_name, vec_type)

            # Создаем истинные метки (числа 0..6)
            raw_themes = [cluster_of(name) for name in doc_names]
            unique_themes = sorted(set(raw_themes))
            theme_map = {t: i for i, t in enumerate(unique_themes)}
            true_labels = np.array([theme_map[t] for t in raw_themes])

            out_dir = os.path.join(OUT, ai_name, vec_type)
            os.makedirs(out_dir, exist_ok=True)

            elbow_df = pd.DataFrame({"k": KS})
            labels_df = pd.DataFrame({"document": doc_names, "true_theme": raw_themes})
            metrics_rows = []
            k_opts = {}
            found, centers, memberships = {}, {}, {}   # для графиков кластеров

            # Сетка: Алгоритм x Мера
            for alg_name in ["kmeans", "cmeans"]:
                func = kmeans if alg_name == "kmeans" else cmeans
                for measure in MEASURES.keys():
                    col_name = f"{alg_name}_{measure}"

                    # 1. Кривая локтя: кластеризация для каждого k (результаты запоминаем)
                    results = {k: func(X, k, measure) for k in KS}
                    inertias = [results[k]["inertia"] for k in KS]
                    elbow_df[col_name] = inertias
                    k_opt = elbow_point(KS, inertias)
                    k_opts[col_name] = k_opt

                    # 2. Оценка для k_opt и k=7 (алгоритмы детерминированы при seed=0,
                    #    поэтому берем уже посчитанные результаты)
                    row = {"alg_measure": col_name, "k_opt": k_opt}
                    for k_val, suffix in [(k_opt, ""), (K_TRUE, "_k7")]:
                        res = results[k_val]
                        ext = external_metrics(true_labels, res["labels"])
                        row[f"silhouette{suffix}"] = silhouette(X, res["labels"], measure)
                        row[f"ARI{suffix}"] = ext["ARI"]
                        row[f"NMI{suffix}"] = ext["NMI"]
                        row[f"purity{suffix}"] = ext["purity"]

                        if suffix == "":
                            # Метки для k_opt
                            labels_df[col_name] = res["labels"]
                            found[col_name] = res["labels"]
                            centers[col_name] = res["centers"]
                            # Матрица принадлежностей c-средних для k_opt
                            if alg_name == "cmeans":
                                memberships[measure] = res["u"]
                                u_df = pd.DataFrame(res["u"], index=doc_names,
                                                    columns=[f"кластер_{j}" for j in range(res["u"].shape[1])])
                                save_csv(u_df, os.path.join(out_dir, f"memberships_cmeans_{measure}.csv"), index=True)
                    metrics_rows.append(row)

            metrics_df = pd.DataFrame(metrics_rows)
            save_csv(metrics_df, os.path.join(out_dir, "metrics.csv"))
            save_csv(elbow_df, os.path.join(out_dir, "elbow_curves.csv"))
            save_csv(labels_df, os.path.join(out_dir, "labels.csv"))

            # Графики локтя: inertia / inertia(k=2), оптимальное k отмечено крестом
            fig, axes = plt.subplots(1, 2, figsize=(15, 5))
            for ax, alg in zip(axes, ["kmeans", "cmeans"]):
                ax.set_title(f"Метод локтя: {'k-средних' if alg == 'kmeans' else 'c-средних'}\n{ai_name} / {vec_type}")
                for measure, kind in MEASURES.items():
                    col = f"{alg}_{measure}"
                    y_vals = elbow_df[col].values / elbow_df[col].iloc[0]
                    line, = ax.plot(KS, y_vals, marker="o", label=f"{measure} ({kind}), k={k_opts[col]}")
                    ax.plot(k_opts[col], y_vals[KS.index(k_opts[col])], "x", color="red", markersize=12, mew=2)
                ax.set_xlabel("число кластеров k")
                ax.set_ylabel("inertia / inertia(k=2)")
                ax.grid(alpha=0.3)
                ax.legend()
            fig.tight_layout()
            fig.savefig(os.path.join(out_dir, "elbow_curves.png"), dpi=130)
            plt.close(fig)

            # Графики кластеров: проекция на плоскость, состав кластеров, принадлежности c-средних
            tag = f"{ai_name} / {vec_type}"
            met = {r["alg_measure"]: {"ARI": r["ARI"]} for r in metrics_rows}
            plots.plot_clusters_pca(os.path.join(out_dir, "clusters_pca.png"), X, true_labels, unique_themes,
                                    found, centers, k_opts, met, tag)
            plots.plot_proximity_mds(os.path.join(out_dir, "clusters_proximity.png"), X, true_labels, unique_themes,
                                     found, centers, k_opts, met, tag)
            plots.plot_contingency(os.path.join(out_dir, "clusters_composition.png"), true_labels,
                                   unique_themes, found, k_opts, tag)
            plots.plot_memberships(os.path.join(out_dir, "memberships_cmeans.png"), true_labels,
                                   unique_themes, doc_names, memberships, k_opts, tag)

            # Данные для итоговой таблицы
            for row in metrics_df.itertuples():
                alg, measure = row.alg_measure.split("_")
                summary_data.append({
                    "нейросеть": ai_name, "тип_векторов": vec_type,
                    "алгоритм": alg, "мера": measure,
                    "k_opt": row.k_opt, "silhouette": row.silhouette, "ARI": row.ARI,
                    "NMI": row.NMI, "purity": row.purity, "ARI_k7": row.ARI_k7, "NMI_k7": row.NMI_k7
                })

    summary_df = pd.DataFrame(summary_data)
    os.makedirs(OUT, exist_ok=True)
    save_csv(summary_df, os.path.join(OUT, "comparison_summary.csv"))
    plots.plot_summary_heatmaps(os.path.join(OUT, "comparison_summary.png"), summary_df)
    print("\n--- FINAL SUMMARY ---")
    print(summary_df.round(3).to_string())


if __name__ == "__main__":
    run_experiment()
