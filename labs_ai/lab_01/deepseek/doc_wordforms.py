import re
from sklearn.feature_extraction.text import TfidfVectorizer

TOKEN_RE = re.compile(r"[А-Яа-яЁёA-Za-z]+(?:-[А-Яа-яЁёA-Za-z]+)*")


def tokenize_wordforms(text: str):
    return [t.lower() for t in TOKEN_RE.findall(text) if len(t) > 1]


def build_doc_wordforms(texts: dict) -> dict:
    doc_ids = list(texts.keys())
    docs = [texts[d] for d in doc_ids]

    vectorizer = TfidfVectorizer(
        tokenizer=tokenize_wordforms,
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
        if row.nnz == 0:
            result[doc_id] = {}
            continue
        cols = row.indices
        vals = row.data
        result[doc_id] = {vocab[c]: float(v) for c, v in zip(cols, vals)}
    return result