import re
import pymorphy3
from sklearn.feature_extraction.text import TfidfVectorizer

TOKEN_RE = re.compile(r"[А-Яа-яЁёA-Za-z]+(?:-[А-Яа-яЁёA-Za-z]+)*")
STOP_POS = {"PREP", "CONJ", "PRCL", "INTJ", "NPRO"}

_morph = pymorphy3.MorphAnalyzer()


def lemma_tokenize(text: str):
    tokens = []
    for t in TOKEN_RE.findall(text):
        t = t.lower()
        if len(t) <= 1:
            continue
        p = _morph.parse(t)[0]
        if p.tag.POS in STOP_POS:
            continue
        tokens.append(p.normal_form)
    return tokens


def build_doc_lemmas(texts: dict) -> dict:
    doc_ids = list(texts.keys())
    docs = [texts[d] for d in doc_ids]

    vectorizer = TfidfVectorizer(
        tokenizer=lemma_tokenize,
        token_pattern=None,
        lowercase=False,
        min_df=1,
        sublinear_tf=True,
    )
    matrix = vectorizer.fit_transform(docs)
    vocab = vectorizer.get_feature_names_out()

    result = {}
    for i, doc_id in enumerate(doc_ids):
        row = matrix.getrow(i)
        cols = row.indices
        vals = row.data
        result[doc_id] = {vocab[c]: float(v) for c, v in zip(cols, vals)}
    return result