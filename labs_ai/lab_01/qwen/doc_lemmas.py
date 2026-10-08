import re
import math
from collections import Counter
import pymorphy3

_morph = pymorphy3.MorphAnalyzer()


def lemma(token):
    return _morph.parse(token)[0].normal_form


def tokenize_and_lemmatize(text):
    return [lemma(t) for t in re.findall(r'[а-яё]+', text.lower())]


def build(texts):
    doc_freq = Counter()
    tf_per_doc = {}

    for doc_name, text in texts.items():
        lemmas = tokenize_and_lemmatize(text)
        counts = Counter(lemmas)
        tf_per_doc[doc_name] = counts
        for w in counts:
            doc_freq[w] += 1

    N = len(texts)
    result = {}
    for doc_name, counts in tf_per_doc.items():
        total = sum(counts.values())
        if total == 0:
            result[doc_name] = {}
            continue
        vec = {}
        for w, c in counts.items():
            tf = c / total
            idf = math.log(N / doc_freq[w])
            weight = round(tf * idf, 6)
            if weight > 0:                 # по ТЗ — только ненулевые веса
                vec[w] = weight
        result[doc_name] = vec
    return result