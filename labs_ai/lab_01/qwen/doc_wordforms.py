import re
import math
from collections import Counter


def tokenize(text):
    return re.findall(r'[а-яё]+', text.lower())


def build(texts):
    doc_freq = Counter()          # df: слово -> число документов
    tf_per_doc = {}               # {doc: Counter(словоформ)}

    for doc_name, text in texts.items():
        tokens = tokenize(text)
        counts = Counter(tokens)
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