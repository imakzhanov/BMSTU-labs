import math
import re
from collections import defaultdict, Counter
from functools import lru_cache
import pymorphy3
from natasha import (
    Segmenter, NewsEmbedding, NewsMorphTagger,
    NewsSyntaxParser, Doc,
)

MIN_PAIR_FREQ = 2
MIN_G2 = 10.83   # ~p<0.001 для 1 степени свободы
STOP_POS = {"PREP", "CONJ", "PRCL", "INTJ", "NPRO"}
WORD_RE = re.compile(r"[а-яёa-z]+(?:-[а-яёa-z]+)*")

_morph = pymorphy3.MorphAnalyzer()

_segmenter = Segmenter()
_emb = NewsEmbedding()
_morph_tagger = NewsMorphTagger(_emb)
_syntax_parser = NewsSyntaxParser(_emb)


@lru_cache(maxsize=None)
def _lemma_or_none(text: str):
    """Лемма (pymorphy3) для обычного слова; None для знаков препинания, цифр,
    однобуквенных токенов и служебных частей речи."""
    if len(text) < 2 or not WORD_RE.fullmatch(text):
        return None
    parse = _morph.parse(text)[0]
    if parse.tag.POS in STOP_POS:
        return None
    return parse.normal_form


def analyze(text: str):
    """Возвращает список токенов: (id, lemma, head_id, rel).
    У токенов без леммы (пунктуация, цифры, служебные слова) lemma = None."""
    doc = Doc(text)
    doc.segment(_segmenter)
    doc.tag_morph(_morph_tagger)
    doc.parse_syntax(_syntax_parser)

    return [(tok.id, _lemma_or_none(tok.text.lower()), tok.head_id, tok.rel)
            for tok in doc.tokens]


def build_word_dependencies(texts: dict) -> dict:
    pair_counts = Counter()           # (w, head) направленные пары
    word_counts = Counter()
    head_counts = Counter()

    dep_pairs_counts = Counter()      # пары (head_lemma, dep_lemma, rel)
    head_lemma_counts = Counter()
    dep_lemma_counts = Counter()
    total_dep_pairs = 0

    for text in texts.values():
        tokens = analyze(text)
        by_id = {tid: (lemma, head, rel) for tid, lemma, head, rel in tokens}

        for tid, lemma, head_id, rel in tokens:
            if lemma is None:
                continue
            word_counts[lemma] += 1

            # контексты: голова и все зависимые
            ctx = []
            if head_id in by_id:
                h_lemma = by_id[head_id][0]
                if h_lemma:
                    ctx.append(h_lemma)
                    head_counts[h_lemma] += 1
            for other_id, (o_lemma, o_head, o_rel) in by_id.items():
                if o_head == tid and o_lemma:
                    ctx.append(o_lemma)

            for c in ctx:
                pair_counts[(lemma, c)] += 1

        # пары для коллокаций
        for tid, lemma, head_id, rel in tokens:
            if lemma is None or rel == "root":
                continue
            if head_id not in by_id:
                continue
            h_lemma = by_id[head_id][0]
            if not h_lemma:
                continue
            dep_pairs_counts[(h_lemma, lemma, rel)] += 1
            head_lemma_counts[h_lemma] += 1
            dep_lemma_counts[lemma] += 1
            total_dep_pairs += 1

    # PPMI по синтаксическим контекстам
    total_pairs = sum(pair_counts.values()) or 1
    total_tokens = sum(word_counts.values()) or 1

    raw_vectors = defaultdict(dict)
    for (w, c), f in pair_counts.items():
        p_wc = f / total_pairs
        p_w = word_counts[w] / total_tokens
        p_c = head_counts.get(c, 0) / total_tokens
        if p_c == 0:
            continue
        pmi = math.log(p_wc / (p_w * p_c) + 1e-12)
        if pmi > 0:
            raw_vectors[w][c] = pmi

    vectors_out = {}
    for w, ctx in raw_vectors.items():
        norm = math.sqrt(sum(v * v for v in ctx.values()))
        if norm == 0:
            continue
        vectors_out[w] = {c: v / norm for c, v in ctx.items()}

    # G² (log-likelihood ratio) для коллокаций
    collocations = []
    N = total_dep_pairs or 1
    for (h, d, rel), f in dep_pairs_counts.items():
        if f < MIN_PAIR_FREQ:
            continue
        f_h = head_lemma_counts[h]
        f_d = dep_lemma_counts[d]
        # таблица 2x2: (h,d), (h,¬d), (¬h,d), (¬h,¬d)
        o11 = f
        o12 = f_h - f
        o21 = f_d - f
        o22 = N - o11 - o12 - o21
        if min(o11, o12, o21, o22) < 0:
            continue
        e11 = f_h * f_d / N
        e12 = f_h * (N - f_d) / N
        e21 = (N - f_h) * f_d / N
        e22 = (N - f_h) * (N - f_d) / N

        g2 = 0.0
        for o, e in ((o11, e11), (o12, e12), (o21, e21), (o22, e22)):
            if o > 0 and e > 0:
                g2 += 2.0 * o * math.log(o / e)

        if g2 < MIN_G2:
            continue
        collocations.append({
            "phrase": f"{h} {d}",
            "freq": int(f),
            "score": round(float(g2), 4),
        })

    collocations.sort(key=lambda x: x["score"], reverse=True)

    return {"vectors": vectors_out, "collocations": collocations}