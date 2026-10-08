import re
from collections import Counter, defaultdict
from functools import lru_cache
from math import log2
from typing import Dict

import pymorphy3
import spacy
from tqdm import tqdm

# Загружаем модель один раз при импорте модуля.
# spaCy используется ТОЛЬКО как синтаксический парсер (границы токенов, head, dep_);
# disable=["ner"] отключает распознавание именованных сущностей для ускорения работы.
nlp = spacy.load("ru_core_news_sm", disable=["ner"])
_morph = pymorphy3.MorphAnalyzer()

MIN_FREQ = 5
STOP_POS = {"PREP", "CONJ", "PRCL", "INTJ", "NPRO"}
WORD_RE = re.compile(r"[а-яёa-z]+(?:-[а-яёa-z]+)*")


@lru_cache(maxsize=None)
def _lemma_or_none(word: str):
    """Лемма через pymorphy3 (по ТЗ морфология — только pymorphy3, а не spaCy .lemma_).
    None для знаков препинания, цифр, однобуквенных токенов и служебных частей речи."""
    word = word.lower()
    if len(word) < 2 or not WORD_RE.fullmatch(word):
        return None
    parse = _morph.parse(word)[0]
    if parse.tag.POS in STOP_POS:
        return None
    return parse.normal_form


def build_dep_vectors_and_collocations(texts: Dict[str, str]) -> Dict:
    """
    Строит векторы слов и коллокации на основе синтаксических зависимостей (spaCy).

    Возвращает:
    {
      "vectors": {"лемма_губернатора": {"тип_связи:лемма_зависимого": частота, ...}, ...},
      "collocations": [{"phrase": "лемма_губернатора лемма_зависимого", "freq": N, "score": PPMI}, ...]
    }
    """
    gov_counts = Counter()          # слово как губернатор (по числу связей)
    dep_counts = Counter()          # слово как зависимое (по числу связей)
    pair_counts = Counter()         # (губернатор, зависимое) -> число связей
    cooccurrence = defaultdict(lambda: defaultdict(int))   # матрица смежности графа

    total_links = 0                 # всего учтённых синтаксических связей

    for content in tqdm(texts.values(), desc="Разбор зависимостей", leave=False):
        doc = nlp(content)
        lemmas = [_lemma_or_none(token.text) for token in doc]

        for token in doc:
            dep_lemma = lemmas[token.i]
            if dep_lemma is None:
                continue

            # Пропускаем корень предложения, чтобы не создавать фиктивные связи
            if token.dep_ == "ROOT":
                continue

            gov_lemma = lemmas[token.head.i]
            # Защита от ошибок разметки, служебных слов и совпадения лемм
            if gov_lemma is None or gov_lemma == dep_lemma:
                continue

            relation = token.dep_
            gov_counts[gov_lemma] += 1
            dep_counts[dep_lemma] += 1
            pair_counts[(gov_lemma, dep_lemma)] += 1
            cooccurrence[gov_lemma][f"{relation}:{dep_lemma}"] += 1
            total_links += 1

    # Если данных недостаточно
    if not cooccurrence or total_links == 0:
        return {"vectors": {}, "collocations": []}

    # Отбор словосочетаний «губернатор + зависимое» по PPMI
    # (раньше сохранялись строки вида «слово --связь--> ...» без второго слова)
    collocations = []
    for (gov, dep), joint_count in pair_counts.items():
        if joint_count < MIN_FREQ:
            continue

        p_xy = joint_count / total_links
        p_gov = gov_counts[gov] / total_links
        p_dep = dep_counts[dep] / total_links

        pmi = log2(p_xy / (p_gov * p_dep))
        ppmi = max(0, pmi)
        if ppmi > 0:
            collocations.append({
                "phrase": f"{gov} {dep}",
                "freq": joint_count,
                "score": round(ppmi, 4)
            })

    collocations.sort(key=lambda x: x["score"], reverse=True)

    vectors = {word: dict(ctxs) for word, ctxs in cooccurrence.items()}

    return {"vectors": vectors, "collocations": collocations}
