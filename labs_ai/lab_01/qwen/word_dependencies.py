import math
import re
from collections import Counter, defaultdict
from functools import lru_cache
import pymorphy3
from natasha import (
    Doc, Segmenter,
    NewsEmbedding, NewsMorphTagger, NewsSyntaxParser,
)

STOP_POS = {"PREP", "CONJ", "PRCL", "INTJ", "NPRO"}
WORD_RE = re.compile(r"[а-яёa-z]+(?:-[а-яёa-z]+)*")

_morph = pymorphy3.MorphAnalyzer()
_emb = NewsEmbedding()
_segmenter = Segmenter()
_morph_tagger = NewsMorphTagger(_emb)
_syntax_parser = NewsSyntaxParser(_emb)


@lru_cache(maxsize=None)
def _lemma_or_none(token_text):
    """Лемма (pymorphy3) для обычного слова; None для знаков препинания, цифр,
    однобуквенных токенов и служебных частей речи."""
    text = token_text.lower()
    if len(text) < 2 or not WORD_RE.fullmatch(text):
        return None
    parse = _morph.parse(text)[0]
    if parse.tag.POS in STOP_POS:
        return None
    return parse.normal_form


def lemma(token_text):
    return _lemma_or_none(token_text)


def build(texts):
    word_contexts = defaultdict(Counter)   # лемма -> Counter связанных лемм
    unigram_counts = Counter()
    pair_counts = Counter()                # (лемма1, лемма2) -> freq

    for text in texts.values():
        doc = Doc(text)
        doc.segment(_segmenter)
        doc.tag_morph(_morph_tagger)
        doc.parse_syntax(_syntax_parser)

        for sent in doc.sents:
            # id -> лемма в пределах предложения
            id2lemma = {}
            for tok in sent.tokens:
                lem = lemma(tok.text)          # None: пунктуация, цифры, служебные слова
                id2lemma[tok.id] = lem
                if lem:
                    unigram_counts[lem] += 1

            for tok in sent.tokens:
                if tok.head_id is None or tok.head_id not in id2lemma:
                    continue
                w = id2lemma[tok.id]
                h = id2lemma[tok.head_id]
                if not w or not h or w == h:
                    continue
                # симметрично для векторов
                word_contexts[w][h] += 1
                word_contexts[h][w] += 1
                # для коллокаций — упорядоченная пара (зависимое, голова)
                pair_counts[(w, h)] += 1

    vectors = {}
    for w, ctx in word_contexts.items():
        total = sum(ctx.values())
        vectors[w] = {c: round(n / total, 6) for c, n in ctx.items()}

    total_uni = sum(unigram_counts.values())
    total_pairs = sum(pair_counts.values())

    collocations = []
    for (w1, w2), freq in pair_counts.items():
        if freq < 2:
            continue
        p1 = unigram_counts[w1] / total_uni
        p2 = unigram_counts[w2] / total_uni
        p12 = freq / total_pairs
        pmi = math.log(p12 / (p1 * p2))
        collocations.append({
            "phrase": f"{w1} {w2}",
            "freq": freq,
            "score": round(pmi, 4),
        })
    collocations.sort(key=lambda x: x["score"], reverse=True)

    return {"vectors": vectors, "collocations": collocations}