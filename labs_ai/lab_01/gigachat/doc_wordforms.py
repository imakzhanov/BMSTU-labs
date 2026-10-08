import re
import math
from collections import defaultdict, Counter
from typing import Dict


def _tokenize(text: str):
    # Находит последовательности букв (русских и латинских), игнорируя регистр
    return [w.lower() for w in re.findall(r'[a-zA-Zа-яА-ЯёЁ]+', text)]


def vectorize_doc_wordforms(texts: Dict[str, str]) -> Dict[str, Dict[str, float]]:
    """
    Строит TF-IDF векторы документов по словоформам.
    Возвращает словарь {имя_файла: {словоформа: вес, ...}, ...}
    Веса округляются до 6 знаков после запятой.
    """
    doc_tokens = {}

    # Этап 1: Токенизация и подсчет term frequency (tf) внутри каждого документа
    for fname, content in texts.items():
        tokens = _tokenize(content)
        if not tokens:
            continue

        tf_counter = Counter(tokens)
        total_terms = len(tokens)

        # Нормировка частоты (term frequency): количество / общее число слов в документе
        doc_tokens[fname] = {word: count / total_terms for word, count in tf_counter.items()}

    if not doc_tokens:
        return {}

    # Этап 2: Подсчет document frequency (df) — в скольких документах встречается слово
    df = Counter()
    for terms in doc_tokens.values():
        unique_words_in_doc = set(terms.keys())
        df.update(unique_words_in_doc)

    N = len(doc_tokens)  # Общее количество документов

    # Этап 3: Вычисление IDF для всего корпуса
    # Используем сглаживание (+1), чтобы избежать деления на ноль для редких слов
    idf = {word: math.log((N + 1) / (freq + 1)) + 1 for word, freq in df.items()}

    # Этап 4: Сборка финальных векторов (TF * IDF)
    result = {}
    for fname, tf_dict in doc_tokens.items():
        features = {}
        for word, tf_val in tf_dict.items():
            weight = tf_val * idf[word]
            # Оставляем только ненулевые веса согласно ТЗ
            if weight > 0:
                features[word] = round(weight, 6)

        if features:
            result[fname] = features

    return result