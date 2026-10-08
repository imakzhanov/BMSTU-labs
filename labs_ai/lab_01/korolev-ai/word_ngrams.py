import pymorphy3
import re
import numpy as np
from collections import Counter, defaultdict
from functools import lru_cache

morph = pymorphy3.MorphAnalyzer()

WINDOW = 2                 # соседей слева и справа для векторов слов
MIN_BIGRAM_FREQ = 3        # коллокации реже этого порога — статистический шум
STOP_POS = {"PREP", "CONJ", "PRCL", "INTJ", "NPRO"}
WORD_RE = re.compile(r'[а-яёa-z]+(?:-[а-яёa-z]+)*')


@lru_cache(maxsize=None)
def _analyze(word):
    parse = morph.parse(word)[0]
    return parse.normal_form, parse.tag.POS


def _lemmas(text):
    """Текст -> леммы (pymorphy3) без служебных частей речи; цифры, знаки и
    служебные символы кодировки в токены не попадают."""
    out = []
    for w in WORD_RE.findall(text.lower()):
        if len(w) < 2:
            continue
        lemma, pos = _analyze(w)
        if pos not in STOP_POS:
            out.append(lemma)
    return out


def get_ngram_vectors(texts):
    word_counts = Counter()
    co_occurrence = defaultdict(Counter)
    bigram_counts = Counter()
    total_bigrams = 0

    # Предварительная обработка и сбор статистики
    for text in texts.values():
        lemmas = _lemmas(text)

        for i, word in enumerate(lemmas):
            word_counts[word] += 1
            # Окно +- WINDOW слов
            for j in range(max(0, i - WINDOW), min(len(lemmas), i + WINDOW + 1)):
                if i != j:
                    co_occurrence[word][lemmas[j]] += 1

        # Коллокации — только упорядоченные пары СОСЕДНИХ слов
        # (раньше брались все пары из окна в обоих порядках: «картина внезапный» и «внезапный картина»)
        for a, b in zip(lemmas, lemmas[1:]):
            bigram_counts[(a, b)] += 1
        total_bigrams += max(len(lemmas) - 1, 0)

    total_words = sum(word_counts.values())

    # Векторы слов: PMI как вес контекста
    vectors = {}
    for word, contexts in co_occurrence.items():
        vec = {}
        for context, count in contexts.items():
            p_w1_w2 = count / total_words
            p_w1 = word_counts[word] / total_words
            p_w2 = word_counts[context] / total_words
            pmi = np.log2(p_w1_w2 / (p_w1 * p_w2))

            if pmi > 0:
                vec[context] = float(pmi)
        vectors[word] = vec

    # Коллокации: PMI соседних слов, с порогом по частоте
    collocations = []
    for (w1, w2), count in bigram_counts.items():
        if count < MIN_BIGRAM_FREQ:
            continue
        p_xy = count / total_bigrams
        p_x = word_counts[w1] / total_words
        p_y = word_counts[w2] / total_words
        pmi = np.log2(p_xy / (p_x * p_y))
        if pmi > 0:
            collocations.append({
                "phrase": f"{w1} {w2}",
                "freq": int(count),
                "score": float(pmi)
            })

    # Сортировка коллокаций по score
    collocations = sorted(collocations, key=lambda x: x['score'], reverse=True)[:1000]

    return {"vectors": vectors, "collocations": collocations}
