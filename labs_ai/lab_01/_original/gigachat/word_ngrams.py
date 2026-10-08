import re
from collections import Counter, defaultdict
from math import log2
from typing import Dict, List

WINDOW_SIZE = 5
MIN_FREQ = 5


def _tokenize(text: str):
    return [w.lower() for w in re.findall(r'[a-zA-Zа-яА-ЯёЁ]+', text)]


def build_word_vectors_and_collocations(texts: Dict[str, str]) -> Dict:
    unigram_counts = Counter()
    bigram_counts = Counter()
    cooccurrence = defaultdict(lambda: defaultdict(int))

    total_windows = 0

    for content in texts.values():
        tokens = _tokenize(content)
        if len(tokens) < WINDOW_SIZE:
            continue

        for i in range(len(tokens) - WINDOW_SIZE + 1):
            window = tokens[i:i + WINDOW_SIZE]
            center_idx = len(window) // 2
            center_word = window[center_idx]

            unigram_counts[center_word] += 1

            context_words = window[:center_idx] + window[center_idx + 1:]
            for ctx in context_words:
                cooccurrence[center_word][ctx] += 1

            # Биграммы внутри окна для поиска коллокаций
            for j in range(len(window) - 1):
                bigram = (window[j], window[j + 1])
                bigram_counts[bigram] += 1

            total_windows += 1

    # Отбор коллокаций по PPMI
    collocations = []
    vocab_size = sum(unigram_counts.values())
    for (w1, w2), joint_count in bigram_counts.items():
        if joint_count < MIN_FREQ:
            continue
        p_xy = joint_count / total_windows
        p_x = unigram_counts[w1] / vocab_size
        p_y = unigram_counts[w2] / vocab_size

        if p_x > 0 and p_y > 0:
            pmi = log2(p_xy / (p_x * p_y))
            ppmi = max(0, pmi)
            if ppmi > 0:
                phrase = f"{w1} {w2}"
                collocations.append({"phrase": phrase, "freq": joint_count, "score": round(ppmi, 4)})

    collocations.sort(key=lambda x: x["score"], reverse=True)

    # Формирование векторов слов (нормировка не требуется по ТЗ, оставляем сырые веса)
    vectors = {}
    for word, contexts in cooccurrence.items():
        vectors[word] = dict(contexts)

    return {"vectors": vectors, "collocations": collocations}