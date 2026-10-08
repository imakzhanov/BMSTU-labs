import math
from collections import Counter, defaultdict
import pymorphy3
from natasha import (
    Doc, Segmenter,
    NewsEmbedding, NewsMorphTagger, NewsSyntaxParser,
)

_morph = pymorphy3.MorphAnalyzer()
_emb = NewsEmbedding()
_segmenter = Segmenter()
_morph_tagger = NewsMorphTagger(_emb)
_syntax_parser = NewsSyntaxParser(_emb)


def lemma(token_text):
    return _morph.parse(token_text.lower())[0].normal_form


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
                lem = lemma(tok.text)
                id2lemma[tok.id] = lem
                unigram_counts[lem] += 1

            for tok in sent.tokens:
                if tok.head_id is None or tok.head_id not in id2lemma:
                    continue
                w = id2lemma[tok.id]
                h = id2lemma[tok.head_id]
                if w == h:
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