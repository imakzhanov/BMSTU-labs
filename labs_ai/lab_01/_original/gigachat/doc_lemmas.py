import re
import math
from collections import defaultdict, Counter
from typing import Dict
from pymorphy3 import MorphAnalyzer

morph = MorphAnalyzer()


def _lemmatize(text: str):
    words = re.findall(r'[a-zA-Zа-яА-ЯёЁ]+', text.lower())
    lemmas = []
    for word in words:
        # Берем первый (самый вероятный) разбор слова
        parsed = morph.parse(word)[0]
        lemmas.append(parsed.normal_form)
    return lemmas


def vectorize_doc_lemmas(texts: Dict[str, str]) -> Dict[str, Dict[str, float]]:
    """
    Строит TF-IDF векторы документов по начальным формам слов (леммам).
    Возвращает словарь {имя_файла: {лемма: вес, ...}, ...}
    Веса округляются до 6 знаков после запятой.
    """
    doc_tokens = {}

    # Этап 1: Лемматизация и подсчет term frequency (tf)
    for fname, content in texts.items():
        lemmas = _lemmatize(content)
        if not lemmas:
            continue

        tf_counter = Counter(lemmas)
        total_terms = len(lemmas)

        # Нормировка частоты (term frequency)
        doc_tokens[fname] = {lemma: count / total_terms for lemma, count in tf_counter.items()}

    if not doc_tokens:
        return {}

    # Этап 2: Подсчет document frequency (df)
    df = Counter()
    for terms in doc_tokens.values():
        unique_lemmas_in_doc = set(terms.keys())
        df.update(unique_lemmas_in_doc)

    N = len(doc_tokens)

    # Этап 3: Вычисление IDF со сглаживанием
    idf = {lemma: math.log((N + 1) / (freq + 1)) + 1 for lemma, freq in df.items()}

    # Этап 4: Сборка финальных векторов (TF * IDF)
    result = {}
    for fname, tf_dict in doc_tokens.items():
        features = {}
        for lemma, tf_val in tf_dict.items():
            weight = tf_val * idf[lemma]
            if weight > 0:
                features[lemma] = round(weight, 6)

        if features:
            result[fname] = features

    return result