"""
Подсчёт верных и ложных детекций и метрик.

Стулья — по КОЛИЧЕСТВУ на картинке (разметка labels.csv: сколько стульев на изображении):
    TP = min(найдено, на_самом_деле)   верные детекции
    FP = max(найдено − на_самом_деле, 0)   ложные детекции
    FN = max(на_самом_деле − найдено, 0)   пропущенные стулья
Эллипс — по НАЛИЧИЮ на картинке (есть / нет), т.к. посчитать «все» эллипсы на фото нельзя однозначно:
    TP — эллипс есть и найден, FP — найден, а его нет, FN — есть, но не найден, TN — нет и не найден.

Метрики:  precision = TP/(TP+FP),  recall = TP/(TP+FN),  F1 = 2PR/(P+R),
          accuracy (только для эллипса, где есть TN) = (TP+TN)/всего.
"""


def prf(tp, fp, fn):
    p = tp / (tp + fp) if tp + fp else 0.0
    r = tp / (tp + fn) if tp + fn else 0.0
    f = 2 * p * r / (p + r) if p + r else 0.0
    return p, r, f


def count_match(found: int, truth: int):
    return min(found, truth), max(found - truth, 0), max(truth - found, 0)


def presence_match(found: int, truth: int):
    """-> (TP, FP, FN, TN) для одной картинки (found и truth — числа; важно только > 0)."""
    f, t = found > 0, truth > 0
    return int(f and t), int(f and not t), int(t and not f), int(not f and not t)
