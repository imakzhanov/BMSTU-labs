"""
Лабораторная 5: классификация документов (вариант 1: логистическая регрессия,
k ближайших соседей, решающее дерево).

Признаки (9 наборов): векторы документов из лабы 1 четырёх нейросетей (doc_wordforms и doc_lemmas)
и эмбеддинги bge-m3. Классы — 7 тем датасета «тексты» (имя подпапки).

Оценка:
  1. стратифицированная 5-fold кросс-валидация на 50 документах датасета (accuracy, macro-F1,
     матрицы ошибок);
  2. внешний тест: обучение на 50 документах, проверка на новых текстах, сгенерированных БЯМ
     и лежащих в  lab_05/generated/<Тема>/*.txt  (если папка пуста — шаг пропускается).

Результаты: output/cv_metrics.csv, output/external_metrics.csv, output/external_predictions.csv,
            output/summary_*.csv, графики *.png, матрицы ошибок output/confusion/.

Запуск:  pip install scikit-learn sentence-transformers matplotlib   (один раз)
         python main.py
"""

import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import classifiers as clf_mod  # noqa: E402
import features  # noqa: E402
import plots  # noqa: E402
from vectors import cluster_of  # noqa: E402

OUT = os.path.join(HERE, "output")


def save(df, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, sep=";", decimal=",", encoding="utf-8-sig", float_format="%.4f")


def safe(name: str) -> str:
    return name.replace("/", "__")


def main() -> None:
    os.makedirs(OUT, exist_ok=True)
    from text_parser import read_texts  # lab_01/text_parser.py
    import embeddings

    train_texts = read_texts()
    new_texts = features.read_generated()
    print(f"Обучающих документов: {len(train_texts)}, новых (внешний тест): {len(new_texts)}")
    classes = sorted({cluster_of(n) for n in train_texts})
    unknown = {cluster_of(n) for n in new_texts} - set(classes)
    if unknown:
        raise SystemExit(f"В generated/ есть темы, которых нет в датасете: {sorted(unknown)}")

    cv_rows, ext_rows, pred_rows = [], [], []
    for name in features.feature_sets():
        print(f"\n=== {name}", flush=True)
        names, X = features.train_set(name, train_texts, embeddings.embed_texts)
        y = np.array([cluster_of(n) for n in names])
        print(f"  обучающая матрица {X.shape}")

        cv_conf = {}
        for cname, make in clf_mod.CLASSIFIERS.items():
            r = clf_mod.cross_validate(make, X, y, classes)
            cv_conf[cname] = r["confusion"]
            cv_rows.append({"набор": name, "классификатор": cname, "признаков": X.shape[1],
                            "accuracy": r["accuracy"], "accuracy_σ": r["accuracy_std"],
                            "macro_F1": r["macro_f1"], "macro_F1_σ": r["macro_f1_std"]})
            save(pd.DataFrame(r["confusion"], index=classes, columns=classes),
                 os.path.join(OUT, "confusion", f"cv_{safe(name)}_{cname}.csv"))
            print(f"  CV {cname:7s} acc={r['accuracy']:.3f}  F1={r['macro_f1']:.3f}")
        plots.plot_confusions(os.path.join(OUT, "confusion", f"cv_{safe(name)}.png"), cv_conf, classes,
                              f"{name}: матрицы ошибок, 5-fold CV на 50 документах")

        if new_texts:
            tr, Xtr, te, Xte = features.train_test_set(name, train_texts, new_texts, embeddings.embed_texts)
            ytr = np.array([cluster_of(n) for n in tr])
            yte = np.array([cluster_of(n) for n in te])
            ext_conf = {}
            for cname, make in clf_mod.CLASSIFIERS.items():
                r = clf_mod.external_test(make, Xtr, ytr, Xte, yte, classes)
                ext_conf[cname] = r["confusion"]
                ext_rows.append({"набор": name, "классификатор": cname, "документов": len(te),
                                 "accuracy": r["accuracy"], "macro_F1": r["macro_f1"]})
                pred_rows += [{"набор": name, "классификатор": cname, "документ": d, "истина": t, "предсказано": p,
                               "верно": int(t == p)} for d, t, p in zip(te, yte, r["y_pred"])]
                print(f"  EXT {cname:7s} acc={r['accuracy']:.3f}  F1={r['macro_f1']:.3f}")
            plots.plot_confusions(os.path.join(OUT, "confusion", f"external_{safe(name)}.png"), ext_conf, classes,
                                  f"{name}: матрицы ошибок, внешний тест ({len(te)} новых текстов)")

    cv_df = pd.DataFrame(cv_rows)
    save(cv_df.set_index(["набор", "классификатор"]), os.path.join(OUT, "cv_metrics.csv"))
    tables, titles = [], []
    for metric in ("accuracy", "macro_F1"):
        t = cv_df.pivot(index="набор", columns="классификатор", values=metric).reindex(features.feature_sets())
        t = t[list(clf_mod.CLASSIFIERS)]
        save(t, os.path.join(OUT, f"summary_cv_{metric}.csv"))
        plots.plot_heatmap(os.path.join(OUT, f"heatmap_cv_{metric}.png"), t, f"{metric}, 5-fold CV (50 документов)")
        if metric == "accuracy":
            tables.append(t)
            titles.append("Кросс-валидация (50 документов): accuracy")

    if ext_rows:
        ext_df = pd.DataFrame(ext_rows)
        save(ext_df.set_index(["набор", "классификатор"]), os.path.join(OUT, "external_metrics.csv"))
        save(pd.DataFrame(pred_rows).set_index(["набор", "классификатор"]), os.path.join(OUT, "external_predictions.csv"))
        for metric in ("accuracy", "macro_F1"):
            t = ext_df.pivot(index="набор", columns="классификатор", values=metric).reindex(features.feature_sets())
            t = t[list(clf_mod.CLASSIFIERS)]
            save(t, os.path.join(OUT, f"summary_external_{metric}.csv"))
            plots.plot_heatmap(os.path.join(OUT, f"heatmap_external_{metric}.png"), t,
                               f"{metric}, внешний тест ({len(new_texts)} новых текстов)")
            if metric == "accuracy":
                tables.append(t)
                titles.append(f"Внешний тест ({len(new_texts)} новых текстов): accuracy")
    plots.plot_bars(os.path.join(OUT, "comparison_accuracy.png"), tables, titles,
                    "Классификаторы и наборы признаков")

    print("\nCV, accuracy:")
    print(cv_df.pivot(index="набор", columns="классификатор", values="accuracy").round(3).to_string())
    if ext_rows:
        print("\nВнешний тест, accuracy:")
        print(pd.DataFrame(ext_rows).pivot(index="набор", columns="классификатор", values="accuracy").round(3).to_string())


if __name__ == "__main__":
    main()
