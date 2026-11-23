"""
Три классификатора по варианту 1 + оценка.

  logreg — логистическая регрессия (многоклассовая, L2-регуляризация, C=10);
  knn    — k ближайших соседей (k=3, косинусная метрика);
  tree   — решающее дерево (критерий Джини, без ограничения глубины).

Перед каждым классификатором строки векторов приводятся к единичной длине (L2-нормировка,
Normalizer без обучения => утечки нет): так сопоставимы наборы нейросетей, у которых
TF-IDF считался по разным формулам (см. лабу 2), а bge-m3 уже нормирован.
"""

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score
from sklearn.model_selection import StratifiedKFold
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import Normalizer
from sklearn.tree import DecisionTreeClassifier

RANDOM_STATE = 42
N_SPLITS = 5

CLASSIFIERS = {
    "logreg": lambda: make_pipeline(Normalizer(), LogisticRegression(C=10, max_iter=5000)),
    "knn":    lambda: make_pipeline(Normalizer(), KNeighborsClassifier(n_neighbors=3, metric="cosine")),
    "tree":   lambda: make_pipeline(Normalizer(), DecisionTreeClassifier(random_state=RANDOM_STATE)),
}
CLASSIFIER_TITLES = {"logreg": "логистическая регрессия", "knn": "k ближайших соседей (k=3)", "tree": "решающее дерево"}


def cross_validate(make_clf, X, y, classes):
    """Стратифицированная 5-fold. -> dict: accuracy/macro-F1 (среднее и σ по фолдам),
    y_pred (предсказание для каждого документа, когда он был в тесте), confusion (7×7)."""
    y = np.asarray(y)
    cv = StratifiedKFold(n_splits=N_SPLITS, shuffle=True, random_state=RANDOM_STATE)
    accs, f1s = [], []
    y_pred = np.empty_like(y)
    for tr, te in cv.split(X, y):
        pred = make_clf().fit(X[tr], y[tr]).predict(X[te])
        y_pred[te] = pred
        accs.append(accuracy_score(y[te], pred))
        f1s.append(f1_score(y[te], pred, average="macro", labels=classes, zero_division=0))
    return {"accuracy": float(np.mean(accs)), "accuracy_std": float(np.std(accs)),
            "macro_f1": float(np.mean(f1s)), "macro_f1_std": float(np.std(f1s)),
            "y_pred": y_pred, "confusion": confusion_matrix(y, y_pred, labels=classes)}


def external_test(make_clf, X_train, y_train, X_test, y_test, classes):
    """Обучение на 50 документах, проверка на новых текстах."""
    y_test = np.asarray(y_test)
    pred = make_clf().fit(X_train, y_train).predict(X_test)
    present = [c for c in classes if c in set(y_test)]
    return {"accuracy": float(accuracy_score(y_test, pred)),
            "macro_f1": float(f1_score(y_test, pred, average="macro", labels=present, zero_division=0)),
            "y_pred": pred, "confusion": confusion_matrix(y_test, pred, labels=classes)}
