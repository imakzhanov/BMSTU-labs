import os
import sys
import json
from pathlib import Path
from tqdm import tqdm

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from text_parser import read_texts

from doc_wordforms import vectorize_doc_wordforms
from doc_lemmas import vectorize_doc_lemmas
from word_ngrams import build_word_vectors_and_collocations
# Имя файла остается прежним
from word_dependencies import build_dep_vectors_and_collocations


def save_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    texts = read_texts()

    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)

    steps = [
        ("Векторизация документов по словоформам...", vectorize_doc_wordforms, "doc_wordforms.json"),
        ("Векторизация документов по леммам...", vectorize_doc_lemmas, "doc_lemmas.json"),
        ("Построение векторов слов на основе n-грамм...", build_word_vectors_and_collocations, "word_ngrams.json"),
        ("Построение векторов слов на основе синтаксических зависимостей...", build_dep_vectors_and_collocations,
         "word_dependencies.json")
    ]

    for desc, func, fname in tqdm(steps, desc="Общий прогресс", unit="шаг"):
        print(f"\n{desc}")
        data = func(texts)
        save_json(data, output_dir / fname)

    print("\nГотово. Результаты сохранены в папку output/")