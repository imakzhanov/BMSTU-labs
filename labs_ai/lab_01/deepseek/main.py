import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from text_parser import read_texts

from doc_wordforms import build_doc_wordforms
from doc_lemmas import build_doc_lemmas
from word_ngrams import build_word_ngrams
from word_dependencies import build_word_dependencies


def save_json(obj, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


def main():
    base = os.path.dirname(os.path.abspath(__file__))
    out_dir = os.path.join(base, "output")
    os.makedirs(out_dir, exist_ok=True)

    texts = read_texts()
    print(f"Прочитано документов: {len(texts)}")

    tasks = [
        ("doc_wordforms.json", build_doc_wordforms),
        ("doc_lemmas.json", build_doc_lemmas),
        ("word_ngrams.json", build_word_ngrams),
        ("word_dependencies.json", build_word_dependencies),
    ]

    for fname, func in tasks:
        print(f"Считаю {fname} ...")
        result = func(texts)
        save_json(result, os.path.join(out_dir, fname))
        print(f"  -> сохранено {fname}")

    print("Готово.")


if __name__ == "__main__":
    main()