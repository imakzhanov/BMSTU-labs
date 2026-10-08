import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from text_parser import read_texts

import doc_wordforms
import doc_lemmas
import word_ngrams
import word_dependencies

texts = read_texts()
print(f"Loaded {len(texts)} documents")

output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
os.makedirs(output_dir, exist_ok=True)

modules = [
    ("doc_wordforms.json",     doc_wordforms),
    ("doc_lemmas.json",        doc_lemmas),
    ("word_ngrams.json",       word_ngrams),
    ("word_dependencies.json", word_dependencies),
]

for filename, module in modules:
    print(f"\n>>> {module.__name__}")
    result = module.build(texts)
    path = os.path.join(output_dir, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"    saved -> {path}")