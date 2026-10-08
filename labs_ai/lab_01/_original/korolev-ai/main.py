import os
import sys
import json

# Добавляем корень проекта в путь для импорта text_parser
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from text_parser import read_texts

# Импортируем наши модули
import doc_wordforms
import doc_lemmas
import word_ngrams
import word_dependencies


def save_json(data, filename):
    output_path = os.path.join(os.path.dirname(__file__), 'output', filename)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def main():
    print("Загрузка текстов...")
    texts = read_texts()

    tasks = [
        (doc_wordforms.get_wordforms_vectors, "doc_wordforms.json"),
        (doc_lemmas.get_lemmas_vectors, "doc_lemmas.json"),
        (word_ngrams.get_ngram_vectors, "word_ngrams.json"),
        (word_dependencies.get_dependency_vectors, "word_dependencies.json"),
    ]

    for func, filename in tasks:
        print(f"Обработка {filename}...")
        result = func(texts)
        save_json(result, filename)
        print(f"Готово: {filename}")


if __name__ == "__main__":
    main()