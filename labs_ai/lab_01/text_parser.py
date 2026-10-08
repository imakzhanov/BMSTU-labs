"""
Общий парсер: читает все документы из папки «тексты» (.txt, .docx, .odt, .html)
и возвращает их в виде чистого текста.

Подключается только в main.py каждой нейросети (папки deepseek/, qwen/, gigachat/, korolev-ai/),
остальные скрипты получают готовый словарь texts от main.py:

    import os, sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from text_parser import read_texts

    texts = read_texts()   # {"Анамнез/анамнез_03.txt": "текст...", ...}
    category = name.split("/")[0]   # тематика = имя подпапки

Проверка парсера (таблица по всем файлам + поиск дубликатов):

    python text_parser.py
"""

import os
import re
import sys

from bs4 import BeautifulSoup
import docx
from docx.table import Table
from docx.text.paragraph import Paragraph
from odf.opendocument import load as odf_load
from odf import teletype

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
TEXTS_DIR = os.path.join(ROOT_DIR, "тексты")


# ---------------------------------------------------------------- чтение форматов

def read_txt(path: str) -> str:
    """UTF-8 (в т.ч. с BOM) или cp1251 — в папке «тексты» встречаются обе кодировки."""
    raw = open(path, "rb").read()
    try:
        return raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        return raw.decode("cp1251")


def read_docx(path: str) -> str:
    """Абзацы и таблицы в порядке следования в документе."""
    document = docx.Document(path)
    parts = []
    for element in document.element.body.iterchildren():
        tag = element.tag.rsplit("}", 1)[-1]
        if tag == "p":
            parts.append(Paragraph(element, document).text)
        elif tag == "tbl":
            for row in Table(element, document).rows:
                parts.append(" ".join(cell.text for cell in row.cells))
    return "\n".join(parts)


def read_odt(path: str) -> str:
    """Абзацы (text:p) и заголовки (text:h) в порядке следования, включая текст
    во вложенных span/ссылках."""
    parts = []

    def walk(node):
        if node.qname[1] in ("p", "h") and node.qname[0].endswith(":text:1.0"):
            parts.append(teletype.extractText(node))
            return
        for child in node.childNodes:
            if child.nodeType == child.ELEMENT_NODE:
                walk(child)

    walk(odf_load(path).text)
    return "\n".join(parts)


def read_html(path: str) -> str:
    """HTML-файлы в папке «тексты» получены из PDF конвертером pdf2htmlEX.
    Пустые <span class="_ _N"> — это кернинг внутри слова; если заменить их
    пробелом, слова рвутся («разв ития»), поэтому они удаляются.
    Каждая строка PDF — <div class="t">; переносы «сло-\\nво» склеиваются."""
    soup = BeautifulSoup(open(path, encoding="utf-8").read(), "lxml")
    for tag in soup(["script", "style", "img", "noscript"]):
        tag.decompose()

    if soup.find("meta", attrs={"name": "generator", "content": "pdf2htmlEX"}):
        for span in soup.select("span._"):
            if not span.get_text():
                span.decompose()
        text = "\n".join(line.get_text() for line in soup.select("div.t"))
        return re.sub(r"(\w)[-\u00ad]\n(\w)", r"\1\2", text)

    return soup.get_text("\n")  # обычный HTML


READERS = {".txt": read_txt, ".docx": read_docx, ".odt": read_odt, ".html": read_html}


def normalize(text: str) -> str:
    text = text.replace("\ufeff", "").replace("\u00ad", "").replace("\xa0", " ")
    text = re.sub(r"(\w)¬\s*(\w)", r"\1\2", text)  # «собира¬ются» — знак переноса в анамнез_07.txt
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r" *\n[\n ]*", "\n", text)
    return text.strip()


# ---------------------------------------------------------------- основной API

def read_document(path: str) -> str:
    ext = os.path.splitext(path)[1].lower()
    return normalize(READERS[ext](path))


def read_texts(texts_dir: str = TEXTS_DIR) -> dict[str, str]:
    """Возвращает {"Категория/файл.ext": текст}, отсортировано по имени."""
    texts = {}
    for dirpath, _, filenames in os.walk(texts_dir):
        for fname in filenames:
            if os.path.splitext(fname)[1].lower() in READERS:
                path = os.path.join(dirpath, fname)
                name = os.path.relpath(path, texts_dir).replace(os.sep, "/")
                texts[name] = read_document(path)
    return dict(sorted(texts.items()))


# ---------------------------------------------------------------- самопроверка

def _report(texts: dict[str, str]) -> None:
    words = {n: re.findall(r"[а-яёa-z]+(?:-[а-яёa-z]+)*", t.lower()) for n, t in texts.items()}
    print(f"{'документ':55s} {'слов':>6s}  начало")
    for name, text in texts.items():
        print(f"{name:55s} {len(words[name]):6d}  {text[:50]!r}")
    print(f"\nДокументов: {len(texts)}, слов всего: {sum(map(len, words.values()))}")

    seen = {}
    for name, text in texts.items():
        key = " ".join(words[name])
        if key in seen:
            print(f"ДУБЛИКАТ: {name} совпадает с {seen[key]}")
        seen.setdefault(key, name)


if __name__ == "__main__":
    _report(read_texts(sys.argv[1] if len(sys.argv) > 1 else TEXTS_DIR))
