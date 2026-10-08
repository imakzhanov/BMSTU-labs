from sklearn.feature_extraction.text import TfidfVectorizer
import re


def get_wordforms_vectors(texts):
    docs = list(texts.values())
    filenames = list(texts.keys())

    # Токенизация простым регулярным выражением (только слова)
    vectorizer = TfidfVectorizer(token_pattern=r'(?u)\b\w\w+\b')
    tfidf_matrix = vectorizer.fit_transform(docs)
    feature_names = vectorizer.get_feature_names_out()

    result = {}
    for i, filename in enumerate(filenames):
        row = tfidf_matrix.getrow(i)
        # Извлекаем только ненулевые веса
        doc_vec = {feature_names[col]: float(val)
                   for col, val in zip(row.indices, row.data)}
        result[filename] = doc_vec

    return result