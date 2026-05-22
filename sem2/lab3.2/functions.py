from tkinter import messagebox
from PIL import Image
from random import randint
import os.path

IMG_PATH = "1.png"
CLASSIFIED_PATH = "2.png"

COLORS = {
    "blue": (0, 0, 255),
    "red": (255, 0, 0),
    "black": (0, 0, 0)
    }

def create_img(width, height, capacity):
    img = Image.new("RGB", (width, height), "white")

    for color in COLORS.values():
        for _ in range(capacity):
            x, y = randint(0, width - 1), randint(0, height - 1)
            img.putpixel((x, y), color)

    img.save(IMG_PATH)
    img.show()


def distance_square(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return (x2 - x1)**2 + (y2 - y1)**2


def classify_img(k):
    if not os.path.exists(IMG_PATH):
        messagebox.showerror("Ошибка", "Файл не существует")
        return

    img =Image.open(IMG_PATH)
    width, height = img.size

    pixels = img.load()

    # разбиваем точки по классам
    black_pixels = [] # (x, y)
    colored_pixels = [] # (color, (x, y))
    for x in range(width):
        for y in range(height):
            color = pixels[x, y]
            if color == COLORS["black"]:
                black_pixels.append((x, y))
            elif color == COLORS["red"] or color == COLORS["blue"]:
                colored_pixels.append((color, (x, y)))

    for black in black_pixels:
        distances = []
        for pixel in colored_pixels:
            color, cords = pixel
            distances.append((distance_square(black, cords), color))

        distances = [i[1] for i in sorted(distances)[:min(k, len(colored_pixels))]]
        red_near = distances.count(COLORS["red"])
        blue_near = distances.count(COLORS["blue"])
        if red_near >= blue_near:
            pixels[black] = COLORS["red"]
        else:
            pixels[black] = COLORS["blue"]

    img.save(CLASSIFIED_PATH)
    img.show()


