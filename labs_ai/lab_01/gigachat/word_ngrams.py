import re
from collections import Counter, defaultdict
from functools import lru_cache
from math import log2
from typing import Dict

import pymorphy3

WINDOW_SIZE = 5          # окно: центральное слово и по (WINDOW_SIZE // 2) соседей с каждой стороны
MIN_FREQ = 5
STOP_POS = {"PREP", "CONJ", "PRCL", "INTJ", "NPRO"}

_morph = pymorphy3.MorphAnalyzer()


@lru_cache(maxsize=None)
def _analyze(word: str):
    parse = _morph.parse(word)[0]
    return parse.normal_form, parse.tag.POS


def _tokenize(text: str):
    """Текст -> леммы (pymorphy3) без служебных частей речи и однобуквенных токенов."""
    out = []
    for w in re.findall(r'[a-zA-Zа-яА-ЯёЁ]+', text):
        w = w.lower()
        if len(w) < 2:
            continue
        lemma, pos = _analyze(w)
        if pos not in STOP_POS:
            out.append(lemma)
    return out


def build_word_vectors_and_collocations(texts: Dict[str, str]) -> Dict:
    unigram_counts = Counter()
    bigram_counts = Counter()
    cooccurrence = defaultdict(lambda: defaultdict(int))

    total_tokens = 0
    total_bigrams = 0
    half = WINDOW_SIZE // 2

    for content in texts.values():
        tokens = _tokenize(content)
        if len(tokens) < 2:
            continue

        # Векторы слов: контексты — соседи в окне
        for i, word in enumerate(tokens):
            for j in range(max(0, i - half), min(len(tokens), i + half + 1)):
                if j != i:
                    cooccurrence[word][tokens[j]] += 1

        unigram_counts.update(tokens)
        total_tokens += len(tokens)

        # Биграммы считаются один раз на каждую пару соседних слов
        # (раньше пара попадала в каждое из перекрывающихся окон и считалась до 4 раз)
        for a, b in zip(tokens, tokens[1:]):
            bigram_counts[(a, b)] += 1
        total_bigrams += len(tokens) - 1

    # Отбор коллокаций по PPMI
    collocations = []
    for (w1, w2), joint_count in bigram_counts.items():
        if joint_count < MIN_FREQ:
            continue
        p_xy = joint_count / total_bigrams
        p_x = unigram_counts[w1] / total_tokens
        p_y = unigram_counts[w2] / total_tokens

        pmi = log2(p_xy / (p_x * p_y))
        ppmi = max(0, pmi)
        if ppmi > 0:
            collocations.append({"phrase": f"{w1} {w2}", "freq": joint_count, "score": round(ppmi, 4)})

    collocations.sort(key=lambda x: x["score"], reverse=True)

    # Формирование векторов слов (нормировка не требуется по ТЗ, оставляем сырые веса)
    vectors = {}
    for word, contexts in cooccurrence.items():
        vectors[word] = dict(contexts)

    return {"vectors": vectors, "collocations": collocations}
