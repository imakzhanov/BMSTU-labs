import re
import math
from collections import defaultdict, Counter
import pymorphy3
import numpy as np

TOKEN_RE = re.compile(r"[А-Яа-яЁёA-Za-z]+(?:-[А-Яа-яЁёA-Za-z]+)*")
STOP_POS = {"PREP", "CONJ", "PRCL", "INTJ", "NPRO"}

WINDOW = 3          # соседи слева/справа
MIN_CONTEXT_FREQ = 3
MIN_BIGRAM_FREQ = 3
MIN_TSCORE = 2.0

_morph = pymorphy3.MorphAnalyzer()


def lemma_tokens(text: str):
    out = []
    for t in TOKEN_RE.findall(text):
        t = t.lower()
        if len(t) <= 1:
            continue
        p = _morph.parse(t)[0]
        if p.tag.POS in STOP_POS:
            continue
        out.append(p.normal_form)
    return out


def build_word_ngrams(texts: dict) -> dict:
    # 1. Лемматизация всех документов
    docs_lemmas = [lemma_tokens(t) for t in texts.values()]

    # 2. Пары (слово, контекст) в окне
    pair_counts = Counter()
    word_counts = Counter()
    context_counts = Counter()

    # для t-score bigram'ов считаем по «линейному» порядку всех токенов
    bigram_counts = Counter()
    unigram_counts = Counter()
    total_bigrams = 0

    for tokens in docs_lemmas:
        n = len(tokens)
        for tok in tokens:
            word_counts[tok] += 1
        for i in range(n):
            w = tokens[i]
            lo = max(0, i - WINDOW)
            hi = min(n, i + WINDOW + 1)
            for j in range(lo, hi):
                if j == i:
                    continue
                c = tokens[j]
                pair_counts[(w, c)] += 1
                context_counts[c] += 1
        for i in range(n - 1):
            bg = (tokens[i], tokens[i + 1])
            bigram_counts[bg] += 1
            total_bigrams += 1

    total_pairs = sum(pair_counts.values()) or 1
    total_tokens = sum(word_counts.values()) or 1

    # 3. PPMI-веса
    vectors = defaultdict(dict)
    for (w, c), f in pair_counts.items():
        if f < MIN_CONTEXT_FREQ:
            continue
        p_wc = f / total_pairs
        p_w = word_counts[w] / total_tokens
        p_c = context_counts[c] / total_tokens
        pmi = math.log(p_wc / (p_w * p_c) + 1e-12)
        ppmi = max(pmi, 0.0)
        if ppmi > 0:
            vectors[w][c] = ppmi

    # L2-нормировка строк
    vectors_out = {}
    for w, ctx in vectors.items():
        norm = math.sqrt(sum(v * v for v in ctx.values()))
        if norm == 0:
            continue
        vectors_out[w] = {c: v / norm for c, v in ctx.items()}

    # 4. Ассоциативные словосочетания (t-score)
    collocations = []
    for (w1, w2), f in bigram_counts.items():
        if f < MIN_BIGRAM_FREQ:
            continue
        f1 = word_counts[w1]
        f2 = word_counts[w2]
        if f1 == 0 or f2 == 0:
            continue
        expected = f1 * f2 / total_tokens
        t = (f - expected) / math.sqrt(f)
        if t < MIN_TSCORE:
            continue
        collocations.append({
            "phrase": f"{w1} {w2}",
            "freq": int(f),
            "score": round(float(t), 4),
        })

    collocations.sort(key=lambda x: x["score"], reverse=True)

    return {"vectors": vectors_out, "collocations": collocations}