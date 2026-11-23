"""
Наборы признаков для классификации (всего 9):
    4 нейросети × {doc_wordforms, doc_lemmas}  — векторы документов из лабы 1  +  bge-m3.

Обучающая выборка — 50 документов датасета «тексты» (класс = тема = имя подпапки).
Тестовая выборка — новые тексты из lab_05/generated/<Тема>/*.txt. Чтобы получить для них
векторы «в том же пространстве», что и для обучающих, код лабы 1 КАЖДОЙ нейросети (doc_wordforms.py,
doc_lemmas.py, без изменений) запускается заново на объединённом наборе «50 + новые»:
словарь признаков и IDF пересчитываются, поэтому внешний тест использует векторы этого
объединённого прогона (и обучающие 50 строк — из него же), а кросс-валидация на 50 документах —
исходные JSON лабы 1.
"""

import importlib.util
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
LAB01 = os.path.join(ROOT, "lab_01")
sys.path.insert(0, os.path.join(ROOT, "lab_02"))
sys.path.insert(0, LAB01)

from vectors import AI_NAMES, VECTOR_TYPES, cluster_of, load_doc_vectors  # noqa: E402

GENERATED_DIR = os.path.join(HERE, "generated")
BGE = "bge-m3"

# (модуль, функция) векторизации в лабе 1 у каждой нейросети — имена разные, т.к. писали разные ИИ
BUILDERS = {
    "deepseek":   {"doc_wordforms": ("doc_wordforms", "build_doc_wordforms"),
                   "doc_lemmas":   ("doc_lemmas", "build_doc_lemmas")},
    "qwen":       {"doc_wordforms": ("doc_wordforms", "build"),
                   "doc_lemmas":   ("doc_lemmas", "build")},
    "gigachat":   {"doc_wordforms": ("doc_wordforms", "vectorize_doc_wordforms"),
                   "doc_lemmas":   ("doc_lemmas", "vectorize_doc_lemmas")},
    "korolev-ai": {"doc_wordforms": ("doc_wordforms", "get_wordforms_vectors"),
                   "doc_lemmas":   ("doc_lemmas", "get_lemmas_vectors")},
}


def feature_sets() -> list:
    """Имена 9 наборов: 'deepseek/doc_wordforms', ..., 'bge-m3'."""
    return [f"{ai}/{vt}" for ai in AI_NAMES for vt in VECTOR_TYPES] + [BGE]


def read_generated() -> dict:
    """{'Тема/файл.txt': текст} из lab_05/generated/<Тема>/*.txt (UTF-8 или cp1251)."""
    texts = {}
    if not os.path.isdir(GENERATED_DIR):
        return texts
    for topic in sorted(os.listdir(GENERATED_DIR)):
        d = os.path.join(GENERATED_DIR, topic)
        if not os.path.isdir(d):
            continue
        for fn in sorted(os.listdir(d)):
            if not fn.lower().endswith(".txt"):
                continue
            raw = open(os.path.join(d, fn), "rb").read()
            try:
                text = raw.decode("utf-8-sig")
            except UnicodeDecodeError:
                text = raw.decode("cp1251")
            if text.strip():
                texts[f"{topic}/{fn}"] = text
    return texts


def to_matrix(raw: dict, names: list):
    """{doc: {term: weight}} -> (features, X [names × features])."""
    features = sorted({t for n in names for t in raw[n]})
    index = {t: j for j, t in enumerate(features)}
    X = np.zeros((len(names), len(features)))
    for i, n in enumerate(names):
        for t, w in raw[n].items():
            X[i, index[t]] = w
    return features, X


def _load_module(ai: str, module: str):
    path = os.path.join(LAB01, ai, f"{module}.py")
    spec = importlib.util.spec_from_file_location(f"lab01_{ai.replace('-', '_')}_{module}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def vectorize_merged(ai: str, vector_type: str, texts: dict) -> dict:
    """Запуск кода лабы 1 нейросети `ai` на словаре texts -> {doc: {term: weight}}."""
    module, func = BUILDERS[ai][vector_type]
    return getattr(_load_module(ai, module), func)(texts)


def train_set(name: str, train_texts: dict, embed=None):
    """Исходные векторы 50 документов. -> (doc_names, X)."""
    if name == BGE:
        vecs = embed(train_texts)
        names = sorted(train_texts)
        return names, np.vstack([vecs[n] for n in names])
    ai, vt = name.split("/")
    names, _, X = load_doc_vectors(ai, vt)
    return names, X


def train_test_set(name: str, train_texts: dict, new_texts: dict, embed=None, vectorizer=vectorize_merged):
    """Для внешнего теста: -> (train_names, X_train, test_names, X_test) в общем пространстве признаков."""
    tr, te = sorted(train_texts), sorted(new_texts)
    if name == BGE:
        vecs = embed({**train_texts, **new_texts})
        return tr, np.vstack([vecs[n] for n in tr]), te, np.vstack([vecs[n] for n in te])
    ai, vt = name.split("/")
    raw = vectorizer(ai, vt, {**train_texts, **new_texts})
    _, M = to_matrix(raw, tr + te)
    return tr, M[:len(tr)], te, M[len(tr):]
