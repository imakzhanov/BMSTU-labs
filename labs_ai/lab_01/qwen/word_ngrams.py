import re
import math
from collections import Counter, defaultdict
from functools import lru_cache
import pymorphy3

WINDOW = 2
MIN_FREQ = 2
STOP_POS = {"PREP", "CONJ", "PRCL", "INTJ", "NPRO"}

_morph = pymorphy3.MorphAnalyzer()


@lru_cache(maxsize=None)
def _analyze(token):
    parse = _morph.parse(token)[0]
    return parse.normal_form, parse.tag.POS


def lemma(token):
    return _analyze(token)[0]


def lemmas_of(text):
    """Текст -> леммы (pymorphy3) без служебных частей речи и однобуквенных токенов,
    чтобы в контексты и словосочетания не попадали «и», «в», «у», «не» и т.п."""
    out = []
    for token in re.findall(r'[а-яё]+', text.lower()):
        if len(token) < 2:
            continue
        lem, pos = _analyze(token)
        if pos not in STOP_POS:
            out.append(lem)
    return out


def build(texts):
    word_contexts = defaultdict(Counter)   # lemma -> Counter(соседних лемм)
    unigram_counts = Counter()
    bigram_counts = Counter()

    for text in texts.values():
        lemmas = lemmas_of(text)
        unigram_counts.update(lemmas)

        for i, w in enumerate(lemmas):
            lo = max(0, i - WINDOW)
            hi = min(len(lemmas), i + WINDOW + 1)
            for j in range(lo, hi):
                if i != j:
                    word_contexts[w][lemmas[j]] += 1

        for i in range(len(lemmas) - 1):
            bigram_counts[(lemmas[i], lemmas[i + 1])] += 1

    # векторы: P(контекст | слово)
    vectors = {}
    for w, ctx in word_contexts.items():
        total = sum(ctx.values())
        vectors[w] = {c: round(n / total, 6)
                      for c, n in ctx.items() if n >= MIN_FREQ}

    # коллокации по PMI
    total_uni = sum(unigram_counts.values())
    total_bi = sum(bigram_counts.values())

    collocations = []
    for (w1, w2), freq in bigram_counts.items():
        if freq < MIN_FREQ:
            continue
        p1 = unigram_counts[w1] / total_uni
        p2 = unigram_counts[w2] / total_uni
        p12 = freq / total_bi
        pmi = math.log(p12 / (p1 * p2))
        collocations.append({
            "phrase": f"{w1} {w2}",
            "freq": freq,
            "score": round(pmi, 4),
        })
    collocations.sort(key=lambda x: x["score"], reverse=True)

    return {"vectors": vectors, "collocations": collocations}