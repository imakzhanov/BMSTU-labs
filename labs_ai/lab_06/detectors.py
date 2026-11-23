"""
Три предобученные нейросети с huggingface.co для поиска стульев (класс «chair» набора COCO).
Все — детекторы объектов, обученные на COCO, но с разной архитектурой:

  facebook/detr-resnet-50   — DETR: CNN ResNet-50 + трансформер, прямое предсказание набора рамок (~160 МБ, нужен timm);
  hustvl/yolos-tiny         — YOLOS: «чистый» Vision Transformer без свёрточной части, самая лёгкая (~25 МБ);
  PekingU/rtdetr_r18vd      — RT-DETR: быстрый гибрид CNN ResNet-18 + трансформер, реального времени (~80 МБ).

Модели скачиваются автоматически при первом запуске и кэшируются (C:\\Users\\<имя>\\.cache\\huggingface).
"""

import os

os.environ.setdefault("HF_HUB_DISABLE_SYMLINKS_WARNING", "1")

import torch
from PIL import Image
from transformers import AutoImageProcessor, AutoModelForObjectDetection

MODELS = {
    "detr-resnet-50": "facebook/detr-resnet-50",
    "yolos-tiny": "hustvl/yolos-tiny",
    "rtdetr-r18vd": "PekingU/rtdetr_r18vd",
}
TARGET_LABEL = "chair"
MIN_SCORE = 0.3        # ниже не сохраняем; порог для метрик выбирается в evaluation.py


class HFDetector:
    def __init__(self, hf_name: str):
        self.processor = AutoImageProcessor.from_pretrained(hf_name)
        self.model = AutoModelForObjectDetection.from_pretrained(hf_name).eval()
        self.chair_ids = [i for i, n in self.model.config.id2label.items() if n == TARGET_LABEL]
        if not self.chair_ids:
            raise RuntimeError(f"В {hf_name} нет класса {TARGET_LABEL!r}")

    @torch.no_grad()
    def detect(self, image: Image.Image):
        """-> [(score, (x1, y1, x2, y2)), ...] — только стулья со score >= MIN_SCORE."""
        inputs = self.processor(images=image, return_tensors="pt")
        outputs = self.model(**inputs)
        res = self.processor.post_process_object_detection(
            outputs, threshold=MIN_SCORE, target_sizes=[image.size[::-1]])[0]
        dets = []
        for score, label, box in zip(res["scores"], res["labels"], res["boxes"]):
            if int(label) in self.chair_ids:
                dets.append((float(score), tuple(float(v) for v in box)))
        return sorted(dets, reverse=True)
