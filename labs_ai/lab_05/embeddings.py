import os
os.environ.setdefault("HF_HUB_DISABLE_SYMLINKS_WARNING", "1")
"""
Векторы документов на основе bge-m3 (BAAI/bge-m3, плотные эмбеддинги, 1024 числа).

Модель грузится через sentence-transformers при первом вызове (~2,2 ГБ, скачивается с
Hugging Face один раз):   pip install sentence-transformers

Эмбеддинги кэшируются в output/embeddings_bge_m3.npz (имя документа -> вектор), поэтому при
повторных запусках модель не грузится, если все тексты уже есть в кэше.
"""

import os

import numpy as np

MODEL_NAME = "BAAI/bge-m3"
MAX_SEQ_LENGTH = 512       # модель умеет до 8192 токенов; 512 — экономия памяти на CPU
HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "output", "embeddings_bge_m3.npz")

_model = None


def _get_model():
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer  # pip install sentence-transformers

        _model = SentenceTransformer(MODEL_NAME)
        _model.max_seq_length = MAX_SEQ_LENGTH
    return _model


def _load_cache() -> dict:
    if not os.path.exists(CACHE):
        return {}
    data = np.load(CACHE, allow_pickle=False)
    return dict(zip(data["names"].tolist(), data["vectors"]))


def embed_texts(texts: dict) -> dict:
    """{имя: текст} -> {имя: вектор bge-m3 единичной длины}. Считает только то, чего нет в кэше."""
    cache = _load_cache()
    missing = [n for n in texts if n not in cache]
    if missing:
        print(f"bge-m3: считаю эмбеддинги для {len(missing)} текстов (в кэше {len(cache)}) ...", flush=True)
        vecs = _get_model().encode([texts[n] for n in missing], batch_size=1, normalize_embeddings=True,
                                   show_progress_bar=True)
        cache.update(dict(zip(missing, np.asarray(vecs, dtype=np.float32))))
        os.makedirs(os.path.dirname(CACHE), exist_ok=True)
        names = sorted(cache)
        np.savez_compressed(CACHE, names=np.array(names), vectors=np.vstack([cache[n] for n in names]))
    return {n: cache[n] for n in texts}
