"""
Лабораторная 6 (компьютерное зрение, вариант 4): найти стулья; найти эллипс.

  стулья  — три предобученные нейросети с huggingface.co (detectors.py), точность по количеству;
  эллипс  — OpenCV без нейросетей (shapes.py), точность по наличию на картинке.
Эталон — labels.csv (размечено вручную; проверь и при необходимости поправь).

Результаты в output/: метрики (CSV), построчные результаты по картинкам, размеченные картинки
output/annotated/<модель>/ и output/annotated/ellipse/, график metrics.png.

Запуск:  pip install torch transformers timm opencv-python pillow numpy pandas matplotlib
         python main.py                       (папка с картинками — DATA_DIR ниже)
         python main.py "D:\\другая\\папка"
"""

import os
import sys

import cv2 as cv
import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import evaluation as ev  # noqa: E402
import shapes  # noqa: E402

DATA_DIR = sys.argv[1] if len(sys.argv) > 1 else r"C:\Users\imakz\Downloads\КомпЗрение\КомпЗрение"
OUT = os.path.join(HERE, "output")
THRESHOLDS = [0.3, 0.5, 0.7]
SHOW_THRESHOLD = 0.5       # при каком пороге рисуются рамки на картинках


def imread(path):
    """cv.imread не открывает пути с кириллицей на Windows — читаем байты сами."""
    return cv.imdecode(np.fromfile(path, dtype=np.uint8), cv.IMREAD_COLOR)


def imwrite(path, img):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    ok, buf = cv.imencode(os.path.splitext(path)[1] or ".jpg", img)
    buf.tofile(path)


def save(df, name):
    os.makedirs(OUT, exist_ok=True)
    df.to_csv(os.path.join(OUT, name), sep=";", decimal=",", encoding="utf-8-sig", index=False, float_format="%.4f")


def load_images(labels):
    return {r.image: imread(os.path.join(DATA_DIR, r.image)) for r in labels.itertuples()}


def run_ellipses(images, labels):
    rows, tp, all_ell = [], [0, 0, 0, 0], {}
    for r in labels.itertuples():
        found = shapes.find_ellipses(images[r.image])
        all_ell[r.image] = found
        m = ev.presence_match(len(found), r.ellipse)
        tp = [a + b for a, b in zip(tp, m)]
        rows.append({"картинка": r.image, "эллипс_есть": r.ellipse, "найдено_эллипсов": len(found),
                     "TP": m[0], "FP": m[1], "FN": m[2], "TN": m[3]})
        imwrite(os.path.join(OUT, "annotated", "ellipse", r.image), shapes.draw_ellipses(images[r.image], found))
    TP, FP, FN, TN = tp
    p, rc, f = ev.prf(TP, FP, FN)
    summary = {"метод": "OpenCV fitEllipse", "TP": TP, "FP": FP, "FN": FN, "TN": TN,
               "precision": p, "recall": rc, "F1": f, "accuracy": (TP + TN) / sum(tp)}
    return pd.DataFrame(rows), summary, all_ell


def run_chairs(images, labels):
    import detectors  # тяжёлый импорт (torch) — только когда нужны нейросети
    from PIL import Image

    det_rows, per_rows, sum_rows = [], [], []
    all_dets = {}      # {модель: {картинка: [(score, box)]}} — для общей картинки
    for short, hf_name in detectors.MODELS.items():
        print(f"\n=== {short} ({hf_name})", flush=True)
        try:
            det = detectors.HFDetector(hf_name)
        except Exception as e:  # noqa: BLE001 — не теряем остальные модели из-за одной
            print(f"  не удалось загрузить модель: {e!r}")
            continue
        found_by_img = {}
        all_dets[short] = found_by_img
        for r in labels.itertuples():
            img = images[r.image]
            dets = det.detect(Image.fromarray(cv.cvtColor(img, cv.COLOR_BGR2RGB)))
            found_by_img[r.image] = dets
            for s, b in dets:
                det_rows.append({"модель": short, "картинка": r.image, "score": s,
                                 "x1": b[0], "y1": b[1], "x2": b[2], "y2": b[3]})
            shown = img.copy()
            for s, (x1, y1, x2, y2) in dets:
                if s >= SHOW_THRESHOLD:
                    cv.rectangle(shown, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), max(2, min(img.shape[:2]) // 250))
                    cv.putText(shown, f"{s:.2f}", (int(x1), max(int(y1) - 5, 15)), cv.FONT_HERSHEY_SIMPLEX,
                               max(0.6, min(img.shape[:2]) / 800), (0, 0, 255), 2)
            imwrite(os.path.join(OUT, "annotated", short, r.image), shown)
            print(f"  {r.image:8s} найдено стульев (≥{SHOW_THRESHOLD}): {sum(s >= SHOW_THRESHOLD for s, _ in dets)}"
                  f"  (в разметке {r.chairs})", flush=True)
        for th in THRESHOLDS:
            tot = [0, 0, 0]
            for r in labels.itertuples():
                n = sum(s >= th for s, _ in found_by_img[r.image])
                m = ev.count_match(n, r.chairs)
                tot = [a + b for a, b in zip(tot, m)]
                per_rows.append({"модель": short, "порог": th, "картинка": r.image, "в_разметке": r.chairs,
                                 "найдено": n, "TP": m[0], "FP": m[1], "FN": m[2]})
            p, rc, f = ev.prf(*tot)
            sum_rows.append({"модель": short, "порог": th, "TP": tot[0], "FP": tot[1], "FN": tot[2],
                             "precision": p, "recall": rc, "F1": f})
    return pd.DataFrame(det_rows), pd.DataFrame(per_rows), pd.DataFrame(sum_rows), all_dets


MODEL_COLORS = [(0, 0, 255), (0, 160, 0), (255, 0, 0), (0, 160, 255)]   # BGR: красный, зелёный, синий, оранжевый


def draw_combined(images, all_dets, all_ell):
    """output/annotated/combined/<картинка>: стулья всех моделей (у каждой свой цвет) + эллипсы (жёлтые)."""
    for name, img in images.items():
        out = img.copy()
        t = max(2, min(img.shape[:2]) // 250)
        for e in all_ell.get(name, []):
            cv.ellipse(out, e, (0, 255, 255), t)
        for k, (model, per_img) in enumerate(all_dets.items()):
            col = MODEL_COLORS[k % len(MODEL_COLORS)]
            for s_, (x1, y1, x2, y2) in per_img.get(name, []):
                if s_ >= SHOW_THRESHOLD:
                    cv.rectangle(out, (int(x1) + k * 2, int(y1) + k * 2), (int(x2) - k * 2, int(y2) - k * 2), col, t)
        # легенда
        y = 30
        for k, model in enumerate(all_dets):
            cv.putText(out, model, (10, y), cv.FONT_HERSHEY_SIMPLEX, max(0.7, min(img.shape[:2]) / 700),
                       MODEL_COLORS[k % len(MODEL_COLORS)], 2)
            y += int(34 * max(1, min(img.shape[:2]) / 700))
        cv.putText(out, "ellipse (OpenCV)", (10, y), cv.FONT_HERSHEY_SIMPLEX, max(0.7, min(img.shape[:2]) / 700),
                   (0, 255, 255), 2)
        imwrite(os.path.join(OUT, "annotated", "combined", name), out)


def plot_metrics(chairs, ell):
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.2), gridspec_kw={"width_ratios": [3, 1.3]})
    ax = axes[0]
    sub = chairs[chairs["порог"] == SHOW_THRESHOLD]
    x = np.arange(len(sub))
    for k, (col, c) in enumerate([("precision", "#1f77b4"), ("recall", "#2ca02c"), ("F1", "#d62728")]):
        ax.bar(x + (k - 1) * 0.26, sub[col], 0.26, label=col, color=c, alpha=0.85)
    ax.set_xticks(x)
    ax.set_xticklabels(sub["модель"])
    ax.set_ylim(0, 1.05)
    ax.set_title(f"Стулья, порог {SHOW_THRESHOLD}")
    ax.legend()
    ax.grid(axis="y", alpha=0.25)
    ax = axes[1]
    vals = [ell["precision"], ell["recall"], ell["F1"], ell["accuracy"]]
    ax.bar(["precision", "recall", "F1", "accuracy"], vals, color=["#1f77b4", "#2ca02c", "#d62728", "#7f7f7f"], alpha=0.85)
    ax.set_ylim(0, 1.05)
    ax.set_title("Эллипс (OpenCV)")
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "metrics.png"), dpi=130)
    plt.close(fig)


def main():
    os.makedirs(OUT, exist_ok=True)
    labels = pd.read_csv(os.path.join(HERE, "labels.csv"), sep=";", encoding="utf-8-sig")
    images = load_images(labels)
    print(f"Картинок: {len(images)} из {DATA_DIR}")

    # 1. стулья — нейросети
    det, per, chairs, all_dets = run_chairs(images, labels)
    if len(chairs):
        save(det, "chairs_detections.csv")
        save(per, "chairs_per_image.csv")
        save(chairs, "chairs_metrics.csv")
        print("\nСтулья:")
        print(chairs.round(3).to_string(index=False))

    # 2. эллипс — OpenCV
    per_ell, ell, all_ell = run_ellipses(images, labels)
    save(per_ell, "ellipse_per_image.csv")
    save(pd.DataFrame([ell]), "ellipse_metrics.csv")
    print("\nЭллипс (OpenCV):", {k: (round(v, 3) if isinstance(v, float) else v) for k, v in ell.items()})

    draw_combined(images, all_dets, all_ell)
    if len(chairs):
        plot_metrics(chairs, ell)
    print(f"\nГотово. Результаты — в папке {OUT}")

if __name__ == "__main__":
    main()
