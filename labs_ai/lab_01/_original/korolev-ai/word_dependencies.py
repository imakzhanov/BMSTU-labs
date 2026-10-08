import pymorphy3
import spacy
from collections import Counter, defaultdict
import numpy as np
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация инструментов
morph = pymorphy3.MorphAnalyzer()
# Загружаем легкую русскую модель spacy
try:
    nlp = spacy.load("ru_core_news_sm")
except OSError:
    logger.error("Модель spacy не найдена. Выполните: python -m spacy download ru_core_news_sm")
    nlp = None


def get_dependency_vectors(texts):
    if nlp is None:
        return {"vectors": {}, "collocations": []}

    co_occurrence = defaultdict(Counter)
    word_counts = Counter()

    for filename, text in texts.items():
        try:
            if not text or not isinstance(text, str):
                continue

            # Обработка текста через spacy
            doc = nlp(text)

            # Создаем список лемм для всех токенов через pymorphy3 (строго по ТЗ)
            # spacy дает свои леммы, но мы используем pymorphy3
            lemmas = []
            for token in doc:
                # Очищаем текст от лишних пробелов
                clean_t = token.text.strip()
                if clean_t:
                    # Лемматизируем через pymorphy3
                    lemmas.append(morph.parse(clean_t)[0].normal_form)
                else:
                    lemmas.append("")

            # Извлечение зависимостей
            for token in doc:
                # Индекс токена в документе spacy (0-based)
                idx = token.i

                if idx < len(lemmas):
                    w_lemma = lemmas[idx]
                    if not w_lemma:
                        continue

                    word_counts[w_lemma] += 1

                    # В spacy token.head — это объект токена, который является управляющим
                    head_token = token.head
                    head_idx = head_token.i

                    if head_idx < len(lemmas):
                        head_lemma = lemmas[head_idx]

                        # Чтобы избежать петель и пустых лемм
                        if head_lemma and w_lemma != head_lemma:
                            # Считаем связь в обе стороны
                            co_occurrence[w_lemma][head_lemma] += 1
                            co_occurrence[head_lemma][w_lemma] += 1

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
            collocations.append({
                "phrase": f"{word} {context}",
                "freq": count,
                "score": float(score)
            })
        vectors[word] = vec

    # Сортировка коллокаций по убыванию score
    collocations = sorted(collocations, key=lambda x: x['score'], reverse=True)[:1000]

    return {"vectors": vectors, "collocations": collocations}