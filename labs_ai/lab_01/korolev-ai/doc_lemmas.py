import pymorphy3
import re
from sklearn.feature_extraction.text import TfidfVectorizer

morph = pymorphy3.MorphAnalyzer()


def preprocess_lemmas(text):
    words = re.findall(r'(?u)\b\w\w+\b', text.lower())
    return " ".join([morph.parse(w)[0].normal_form for w in words])


def get_lemmas_vectors(texts):
    filenames = list(texts.keys())
    lemmatized_docs = [preprocess_lemmas(t) for t in texts.values()]

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(lemmatized_docs)
    feature_names = vectorizer.get_feature_names_out()

    result = {}
    for i, filename in enumerate(filenames):
        row = tfidf_matrix.getrow(i)
        doc_vec = {feature_names[col]: float(val)
                   for col, val in zip(row.indices, row.data)}
        result[filename] = doc_vec

    return result