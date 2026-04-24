from tkinter import messagebox
from PIL import Image
from tkinter import filedialog as fd

# Возвращает абсолютный путь до файла, или None при ошибке
def open_file():
    filename = fd.askopenfilename(title="Выберите фото для скрытия сообщения")
    if filename.split('.')[-1] != "bmp":
        messagebox.showerror("Ошибка", "Выбран не bpm файл")
        return None
    return filename

# Возвращает абсолютный путь до файла, или None при ошибке
def save_file():
    filename = fd.asksaveasfilename(title="Выберите куда сохранить", defaultextension=".bmp")
    if filename.split('.')[-1] != "bmp":
        messagebox.showerror("Ошибка", "Выбран не bpm файл")
        return None
    return filename

# по текстовому сообщению возвращает список его битов
def encode_message_to_bit(message):
    bit_message = []
    byte_message = message.encode("ASCII") + b'\x00'
    for byte in byte_message:
        bit_message += list(int(b) for b in bin(byte)[2:].zfill(8))
    return bit_message

# изменяет младший бит в байте
def change_bit(byte: int, bit: int):
    return byte & ~1 | bit


def hide_message(message):
    filename = open_file()
    if filename == None:
        return

    bit_message = encode_message_to_bit(message)

    img = Image.open(filename)
    width, height = img.size

    if (len(bit_message) > width * height * 8 / 3):
        messagebox.showerror("Ошибка", "Невозможно закодировать, превышена длина сообщения")
        return

    pixels = img.tobytes()

    new_pixels = []
    message_index = 0
    pixel_index = 0
    for i in range(0, len(pixels), 3):
        pixel = [pixels[i], pixels[i + 1], pixels[i + 2]]
        if message_index < len(bit_message):
            pixel[0] = change_bit(pixel[0], bit_message[message_index])
            message_index += 1
            pixel[1] = change_bit(pixel[1], bit_message[message_index])
            message_index += 1
            if (pixel_index + 1) % 3 != 0: # байт синего цвета каждого 3 пикселя не меняется
                pixel[2] = change_bit(pixel[2], bit_message[message_index])
                message_index += 1
        pixel_index += 1
        new_pixels.append(tuple(pixel))

    img.putdata(new_pixels)
    path_to_save = save_file()
    if path_to_save:
        img.save(path_to_save)


def get_message(label):
    filename = open_file()
    if filename == None:
        return

    message = ''
    img = Image.open(filename)
    pixels = img.tobytes()

    for i in range(0, len(pixels), 9):
        byte = ''
        for j in range(i, i + 8):
            byte += bin(pixels[j])[-1]

        if byte == '0' * 8:
            break
        message += chr(int(byte, 2))

    label.config(text=message)

