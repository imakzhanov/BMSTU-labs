import pymorphy3
import re
import spacy
from collections import Counter, defaultdict
from functools import lru_cache
import numpy as np
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация инструментов
morph = pymorphy3.MorphAnalyzer()
# Загружаем легкую русскую модель spacy (используется только как синтаксический парсер)
try:
    nlp = spacy.load("ru_core_news_sm")
except OSError:
    logger.error("Модель spacy не найдена. Выполните: python -m spacy download ru_core_news_sm")
    nlp = None

MIN_PAIR_FREQ = 3          # словосочетания реже этого порога — статистический шум
STOP_POS = {"PREP", "CONJ", "PRCL", "INTJ", "NPRO"}
WORD_RE = re.compile(r"[а-яёa-z]+(?:-[а-яёa-z]+)*")


@lru_cache(maxsize=None)
def _lemma_or_none(word):
    """Лемма через pymorphy3 (строго по ТЗ). None для знаков препинания, цифр,
    однобуквенных токенов и служебных частей речи."""
    word = word.lower()
    if len(word) < 2 or not WORD_RE.fullmatch(word):
        return None
    parse = morph.parse(word)[0]
    if parse.tag.POS in STOP_POS:
        return None
    return parse.normal_form


def get_dependency_vectors(texts):
    if nlp is None:
        return {"vectors": {}, "collocations": []}

    co_occurrence = defaultdict(Counter)
    word_counts = Counter()
    gov_counts = Counter()          # слово как губернатор (по числу связей)
    dep_counts = Counter()          # слово как зависимое (по числу связей)
    pair_counts = Counter()         # (губернатор, зависимое) -> число связей
    total_links = 0

    for filename, text in texts.items():
        try:
            if not text or not isinstance(text, str):
                continue

            # Обработка текста через spacy (только парсинг), леммы — через pymorphy3
            doc = nlp(text)
            lemmas = [_lemma_or_none(token.text) for token in doc]

            # Извлечение зависимостей
            for token in doc:
                w_lemma = lemmas[token.i]
                if w_lemma is None:
                    continue

                word_counts[w_lemma] += 1

                # В spacy token.head — это объект токена, который является управляющим
                head_lemma = lemmas[token.head.i]

                # Чтобы избежать петель (у корня head — он сам), служебных слов и пунктуации
                if head_lemma is not None and w_lemma != head_lemma:
                    # Считаем связь в обе стороны (для векторов слов)
                    co_occurrence[w_lemma][head_lemma] += 1
                    co_occurrence[head_lemma][w_lemma] += 1

                    # Направленная пара (губернатор, зависимое) — для коллокаций
                    pair_counts[(head_lemma, w_lemma)] += 1
                    gov_counts[head_lemma] += 1
                    dep_counts[w_lemma] += 1
                    total_links += 1

        except Exception as e:
            logger.error(f"Ошибка при обработке файла {filename}: {e}")
            continue

    # Формирование финальных структур данных
    vectors = {}
    collocations = []

    for word, contexts in co_occurrence.items():
        vec = {}
        w_freq = word_counts[word]

        for context, count in contexts.items():
            # Формула веса: отношение логарифма частоты связи к логарифму частоты слова
            denom = np.log2(w_freq + 1)
            score = np.log2(count + 1) / denom if denom != 0 else 0

            vec[context] = float(score)
        vectors[word] = vec

    # Коллокации: направленные пары «губернатор зависимое», отбор по PMI с порогом по частоте
    # (раньше score = отношение логарифмов частот — это не мера ассоциации, а каждая пара
    # попадала в список дважды, в обоих порядках)
    for (gov, dep), count in pair_counts.items():
        if count < MIN_PAIR_FREQ:
            continue
        p_xy = count / total_links
        p_gov = gov_counts[gov] / total_links
        p_dep = dep_counts[dep] / total_links
        pmi = np.log2(p_xy / (p_gov * p_dep))
        if pmi > 0:
            collocations.append({
                "phrase": f"{gov} {dep}",
                "freq": int(count),
                "score": float(pmi)
            })

    # Сортировка коллокаций по убыванию score
    collocations = sorted(collocations, key=lambda x: x['score'], reverse=True)[:1000]

    return {"vectors": vectors, "collocations": collocations}
