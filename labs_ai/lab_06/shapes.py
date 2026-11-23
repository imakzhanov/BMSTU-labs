"""
Поиск эллипсов средствами OpenCV (классическое компьютерное зрение, без нейросетей).

Алгоритм:
  1. серое изображение, размытие по Гауссу, детектор границ Canny (пороги от медианы яркости);
  2. все контуры границ (cv.findContours);
  3. для каждого достаточно длинного контура — cv.fitEllipse (метод наименьших квадратов);
  4. контур принимается за эллипс, если он ХОРОШО ложится на подогнанный эллипс:
       - невязка  mean|r − 1| < MAX_ERR, где r = расстояние точки до центра в системе осей эллипса
         (для идеального эллипса r = 1 во всех точках);
       - угловое покрытие: контур занимает не менее MIN_COVER доли окружности эллипса
         (отсекает короткие дуги, которые подгоняются под «эллипс» почти всегда);
       - размер полуосей не меньше MIN_AXIS_FRAC от меньшей стороны картинки, вытянутость ≤ MAX_ASPECT;
  5. дубликаты (почти совпадающие эллипсы от внутренней и внешней стороны линии) удаляются.
"""

import cv2 as cv
import numpy as np

MAX_SIDE = 900          # большие картинки уменьшаются — ускорение и устойчивость к шуму
MAX_ERR = 0.08
MIN_COVER = 0.75
BLUR_SIZES = (5, 11)       # два масштаба сглаживания: мелкие и крупные контуры
MIN_AXIS_FRAC = 0.04
MAX_ASPECT = 4.0
MIN_POINTS = 40


def _canny(gray):
    med = float(np.median(gray))
    lo, hi = int(max(0, 0.66 * med)), int(min(255, 1.33 * med))
    return cv.Canny(gray, lo, max(hi, lo + 40))


def _fit_quality(pts, ellipse):
    (cx, cy), (d1, d2), ang = ellipse
    a, b = d1 / 2.0, d2 / 2.0
    t = np.deg2rad(ang)
    x, y = pts[:, 0] - cx, pts[:, 1] - cy
    u = x * np.cos(t) + y * np.sin(t)
    v = -x * np.sin(t) + y * np.cos(t)
    r = np.sqrt((u / a) ** 2 + (v / b) ** 2)
    err = float(np.mean(np.abs(r - 1.0)))
    phi = np.arctan2(v / b, u / a)
    bins = np.unique(((phi + np.pi) / (2 * np.pi) * 36).astype(int) % 36)
    return err, len(bins) / 36.0


def _is_rectangle(c):
    """Контур прямоугольника/ромба (блок-схемы): 4 угла по approxPolyDP и контур заполняет свой минимальный
    прямоугольник — это не эллипс, даже если fitEllipse его «съедает» с большой невязкой."""
    per = cv.arcLength(c, True)
    approx = cv.approxPolyDP(c, 0.02 * per, True)
    if len(approx) != 4:
        return False
    (_, _), (w, h), _ = cv.minAreaRect(c)
    return w * h > 0 and cv.contourArea(c) / (w * h) > 0.7


def find_ellipses(img_bgr, max_err=MAX_ERR, min_cover=MIN_COVER):
    """-> список эллипсов [((cx, cy), (d1, d2), angle), ...] в координатах исходной картинки."""
    h, w = img_bgr.shape[:2]
    k = min(1.0, MAX_SIDE / max(h, w))
    img = cv.resize(img_bgr, None, fx=k, fy=k, interpolation=cv.INTER_AREA) if k < 1 else img_bgr
    gray0 = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    contours = []
    for ks in BLUR_SIZES:
        edges = _canny(cv.GaussianBlur(gray0, (ks, ks), 0))
        contours += cv.findContours(edges, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)[0]
    min_axis = MIN_AXIS_FRAC * min(img.shape[:2])
    found = []
    for c in contours:
        if len(c) < MIN_POINTS or _is_rectangle(c):
            continue
        pts = c[:, 0, :].astype(np.float64)
        try:
            e = cv.fitEllipse(c)
        except cv.error:
            continue
        (cx, cy), (d1, d2), ang = e
        a, b = max(d1, d2) / 2, min(d1, d2) / 2
        if b < min_axis or a / max(b, 1e-6) > MAX_ASPECT:
            continue
        err, cover = _fit_quality(pts, e)
        if err < max_err and cover >= min_cover:
            found.append((e, err))
    found.sort(key=lambda t: t[1])
    kept = []
    for e, _ in found:                                   # подавление дубликатов
        (cx, cy), (d1, d2), _a = e
        s = (d1 + d2) / 2
        if all(np.hypot(cx - k2[0][0], cy - k2[0][1]) > 0.35 * min(s, (k2[1][0] + k2[1][1]) / 2) for k2 in kept):
            kept.append(e)
    return [((cx / k, cy / k), (d1 / k, d2 / k), ang) for (cx, cy), (d1, d2), ang in kept]


def draw_ellipses(img_bgr, ellipses, color=(0, 0, 255)):
    out = img_bgr.copy()
    for e in ellipses:
        cv.ellipse(out, e, color, max(2, min(out.shape[:2]) // 300))
    return out
