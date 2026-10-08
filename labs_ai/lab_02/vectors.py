"""
Загрузка векторов документов из выхлопа лабы 1 (labs_ai/lab_01/<нейросеть>/output/*.json).

Каждая нейросеть в лабе 1 (deepseek, qwen, gigachat, korolev-ai) для каждого
документа уже посчитала вектор и сохранила его как разреженный словарь
{"термин": вес, ...} — в двух вариантах: doc_wordforms.json (по словоформам)
и doc_lemmas.json (по леммам, через pymorphy3). Здесь эти словари переводятся
в плотную матрицу [документы × термины] над общим для всех документов набором
признаков (объединение всех терминов; там, где термина в документе нет, вес — 0).

Кластер документа не строится заново — тема уже задана в самом датасете
(имя подпапки в «тексты»), она читается прямо из ключа словаря:
"Анамнез/анамнез_01.docx" -> кластер "Анамнез".
"""

import json
import os

import numpy as np

LAB01_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "lab_01")

AI_NAMES = ["deepseek", "qwen", "gigachat", "korolev-ai"]
VECTOR_TYPES = ["doc_wordforms", "doc_lemmas"]


def _json_path(ai_name: str, vector_type: str) -> str:
    return os.path.join(LAB01_DIR, ai_name, "output", f"{vector_type}.json")


def load_doc_vectors(ai_name: str, vector_type: str):
    """-> (doc_names, features, X). X — np.ndarray [документы × термины],
    восстановленная из разреженных словарей выхлопа лабы 1 (labs_ai/lab_01)."""
    path = _json_path(ai_name, vector_type)
    with open(path, encoding="utf-8") as f:
        raw = json.load(f)  # {"Категория/файл.ext": {"термин": вес, ...}, ...}

    doc_names = sorted(raw)
    features = sorted({term for vec in raw.values() for term in vec})
    index = {term: j for j, term in enumerate(features)}

    X = np.zeros((len(doc_names), len(features)))
    for i, name in enumerate(doc_names):
        for term, weight in raw[name].items():
            X[i, index[term]] = weight
    return doc_names, features, X


def cluster_of(doc_name: str) -> str:
    """Кластер документа = имя подпапки — тема уже задана в датасете, не вычисляется."""
    return doc_name.split("/")[0]


def build_cluster_vectors(doc_names: list[str], X):
    """-> (cluster_names, C), C — np.ndarray [кластеры × термины], строки — центроиды
    (среднее векторов документов, попавших в кластер)."""
    labels = np.array([cluster_of(n) for n in doc_names])
    cluster_names = sorted(set(labels))
    C = np.vstack([X[labels == c].mean(axis=0) for c in cluster_names])
    return cluster_names, C
