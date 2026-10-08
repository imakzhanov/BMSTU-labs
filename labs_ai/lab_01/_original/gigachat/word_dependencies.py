import re
from collections import Counter, defaultdict
from math import log2
from typing import Dict
import spacy
from tqdm import tqdm

# Загружаем модель один раз при импорте модуля.
# disable=["ner"] отключает распознавание именованных сущностей для ускорения работы.
nlp = spacy.load("ru_core_news_sm", disable=["ner"])

MIN_FREQ = 5


def _clean_token(token: str):
    return re.sub(r'[^a-zA-Zа-яА-ЯёЁ]', '', token.lower())


def build_dep_vectors_and_collocations(texts: Dict[str, str]) -> Dict:
    """
    Строит векторы слов и коллокации на основе синтаксических зависимостей (spaCy).

    Возвращает:
    {
      "vectors": {"лемма_губернатора": {"тип_связи:лемма_зависимого": вес, ...}, ...},
      "collocations": [{"phrase": "слово --связь--> слово", "freq": N, "score": PPMI}, ...]
    }
    """
    gov_counts = Counter()  # Частота слова как губернатора
    rel_pair_counts = Counter()  # Частота пары (губернатор, тип_связи)
    cooccurrence = defaultdict(lambda: defaultdict(int))  # Матрица смежности графа

    total_tokens_processed = 0  # База для вероятностей PMI

    # Используем pipe для потоковой обработки списка текстов (это самый быстрый способ в spaCy)
    for content in tqdm(texts.values(), desc="Разбор зависимостей", leave=False):
        doc = nlp(content)

        sent_token_count = 0
        for token in doc:
            if not token.is_alpha or token.is_punct or token.is_space:
                continue

            clean_lemma = _clean_token(token.lemma_)
            if not clean_lemma:
                continue

            sent_token_count += 1

            # Пропускаем корень предложения, чтобы не создавать фиктивные связи
            if token.dep_ == "ROOT":
                continue

            governor = token.head
            gov_lemma = _clean_token(governor.lemma_)
            dep_lemma = clean_lemma
            relation = token.dep_

            # Защита от ошибок разметки или совпадения форм
            if not gov_lemma or not dep_lemma or gov_lemma == dep_lemma:
                continue

            gov_counts[gov_lemma] += 1
            rel_pair_counts[(gov_lemma, relation)] += 1
            key = f"{relation}:{dep_lemma}"
            cooccurrence[gov_lemma][key] += 1

        total_tokens_processed += sent_token_count

    # Если данных недостаточно
    if not cooccurrence or total_tokens_processed == 0:
        return {"vectors": {}, "collocations": []}

    # Вычисление PPMI для отбора неслучайных связей
    collocations = []
    total_rel_pairs = sum(rel_pair_counts.values())

    for (gov, rel), joint_count in rel_pair_counts.items():
        if joint_count < MIN_FREQ:
            continue

        p_xy = joint_count / total_tokens_processed
        p_gov = gov_counts[gov] / total_tokens_processed

        # Условная вероятность типа связи при данном губернаторе
        p_rel_given_gov = rel_pair_counts[(gov, rel)] / gov_counts[gov]

        if p_xy > 0 and p_gov > 0 and p_rel_given_gov > 0:
            pmi = log2(p_xy / (p_gov * p_rel_given_gov))
            ppmi = max(0, pmi)
            if ppmi > 0:
                phrase = f"{gov} --{rel}--> ..."
                collocations.append({
                    "phrase": phrase,
                    "freq": joint_count,
                    "score": round(ppmi, 4)
                })

    collocations.sort(key=lambda x: x["score"], reverse=True)

    vectors = {word: dict(ctxs) for word, ctxs in cooccurrence.items()}

    return {"vectors": vectors, "collocations": collocations}