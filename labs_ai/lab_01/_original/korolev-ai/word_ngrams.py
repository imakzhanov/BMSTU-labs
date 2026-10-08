import pymorphy3
import re
import numpy as np
from collections import Counter, defaultdict

morph = pymorphy3.MorphAnalyzer()


def get_ngram_vectors(texts):
    word_counts = Counter()
    co_occurrence = defaultdict(Counter)

    # Предварительная обработка и сбор статистики
    all_docs_lemmas = []
    for text in texts.values():
        words = re.findall(r'(?u)\b\w\w+\b', text.lower())
        lemmas = [morph.parse(w)[0].normal_form for w in words]
        all_docs_lemmas.append(lemmas)

        for i, word in enumerate(lemmas):
            word_counts[word] += 1
            # Окно +- 2 слова
            for j in range(max(0, i - 2), min(len(lemmas), i + 3)):
                if i != j:
                    co_occurrence[word][lemmas[j]] += 1

    # Расчет векторов и коллокаций
    total_words = sum(word_counts.values())
    vectors = {}
    collocations = []

    # Считаем только для слов, которые встречаются достаточно часто
    for word, contexts in co_occurrence.items():
        vec = {}
        for context, count in contexts.items():
            # PMI как мера веса контекста
            p_w1_w2 = count / total_words
            p_w1 = word_counts[word] / total_words
            p_w2 = word_counts[context] / total_words
            pmi = np.log2(p_w1_w2 / (p_w1 * p_w2))

            if pmi > 0:
                vec[context] = float(pmi)
                # Для коллокаций берем только пары
                collocations.append({
                    "phrase": f"{word} {context}",
                    "freq": count,
                    "score": float(pmi)
                })
        vectors[word] = vec

    # Сортировка коллокаций по score
    collocations = sorted(collocations, key=lambda x: x['score'], reverse=True)[:1000]

    return {"vectors": vectors, "collocations": collocations}