from PIL import Image


path = "C:/Users/imakz/Downloads/image.bmp"
res = "C:/Users/imakz/Downloads/res_image.bmp"


text = input()
byte_text = text.encode('UTF-8') + b'\x00'

print(list(byte_text))
text_len = len(byte_text) * 8  # длина сообщения в битах

# -------------
img = Image.open(path).convert("RGB")
width, height = img.size

if (width * height * 3 < text_len):
    print("Невозможно закодировать, превышена длина сообщения")

print("Размер изображения: ", width, height)

# Кодирование

pixels = list(img.tobytes())
print(pixels[0])

'''
pix_index = 0

for byte in byte_text: # проходим по всем байтам сообщения
    bits = list(int(b) for b in bin(byte)[2:].zfill(8)) # список битов текущего байта
    for i in range(9):
        if i != 8:
            pixels[pix_index] = (pixels[pix_index] & ~1) | bits[i]
        pix_index += 1


new_pixels = []
for i in range(0, len(pixels), 3):
    new_pixels.append((pixels[i], pixels[i + 1], pixels[i + 2]))


img.putdata(new_pixels)
img.save(res)



def get_lsb(value):
    return str(value & 1)

def decode_text_3px(image_path):
    img = Image.open(image_path).convert("RGB")
    pixels = list(img.getdata())

    result = []

    for i in range(0, len(pixels), 3):
        if i + 2 >= len(pixels):
            break

        block = []
        block.extend(pixels[i])
        block.extend(pixels[i + 1])
        block.extend(pixels[i + 2])

        bits8 = ''.join(get_lsb(block[j]) for j in range(8))
        end_flag = get_lsb(block[8])

        result.append(chr(int(bits8, 2)))

        if end_flag == '1':
            break

    return ''.join(result)

print(decode_text_3px(res))


'''